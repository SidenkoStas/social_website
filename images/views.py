from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from actions.utils import create_action
import redis
from django.conf import settings

red = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
    )

@login_required
def create_image(request):
    """
    Представление для создания нового изображения с авторизацией.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: Ответ с рендером шаблона.

    Поведение:
        - При POST-запросе:
            1. Создаёт форму `ImageCreateForm` с данными из `request.POST`.
            2. Если форма валидна:
                - Сохраняет изображение с привязкой к текущему пользователю.
                - Отправляет сообщение об успехе.
                - Перенаправляет на URL успешного завершения.
            3. Если форма невалидна:
                - Создаёт новую форму с данными из `request.GET`.
        - При других методах:
            - Возвращает пустую форму.
    """
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "Добавлено изображение", new_image)
            messages.success(request, "Изображение успешно добавлено!")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request, "images/create.html", {"section": "images", "form": form}
        )

def image_detail(request, id, slug):
    """
    Отображает детали конкретного изображения.

    Эта функция-представление (view) получает объект изображения по его идентификатору (id)
    и слагу (slug). Если объект не найден, возвращается HTTP-ответ 404. Иначе отображается
    шаблон `images/detail.html` с контекстом, включающим текущее изображение и раздел.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        id (int): Уникальный идентификатор изображения.
        slug (str): URL-дружественный идентификатор изображения.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с контекстом.

    Raises:
        Http404: Если изображение с указанными id и slug не существует.
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = red.incr(f"image:{image.id}:views")
    red.zincrby("image_ranking", 1, image.id)
    return render(
        request, "images/detail.html",
        {"section": "images", "image": image, "total_views": total_views}
        )

@login_required
@require_POST
def image_like(request):
    """
    Обрабатывает POST-запрос для лайка/дизлайка изображения.

    Функция принимает ID изображения и действие (like/dislike) из POST-данных,
    проверяет существование изображения и выполняет соответствующее действие:
    добавляет или удаляет текущего пользователя из списка лайков.

    Parameters:
        request (HttpRequest): POST-запрос, содержащий:
            - 'id' (str): Идентификатор изображения.
            - 'action' (str): Действие ('like' или 'dislike').

    Returns:
        JsonResponse: JSON-ответ со статусом 'ok' при успешной операции,
                      'error' при отсутствии данных или ошибке.

    Raises:
        Image.DoesNotExist: Если изображение с указанным ID не найдено.
    """
    image_id = request.POST.get("id")
    action = request.POST.get("action")

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "Понравилось", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})

@login_required
def image_list(request):
    """
    Отображает список изображений с поддержкой пагинации и фильтрации.

    Функция загружает все объекты модели `Image`, разбивает их на страницы по 8 элементов
    и отображает соответствующий HTML-шаблон. Если запрос содержит параметр `images_only`,
    возвращается упрощённый ответ (пустая строка при ошибке или минималистичный шаблон).

    Параметры:
        request (HttpRequest): HTTP-запрос, содержащий GET-параметры `page` и `images_only`.

    Возвращает:
        HttpResponse: Отрендеренный HTML-шаблон с изображениями или пустую строку при ошибке.

    Исключения:
        PageNotAnInteger: Если номер страницы не является целым числом.
        EmptyPage: Если запрошенная страница выходит за границы диапазона.

    Пример использования:
        GET /images/?page=2&images_only=true
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get("images_only")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            "images/list_images.html",
            {"section": "images", "images": images}
            )
    return render(
        request,
        "images/list.html",
        {"section": "images", "images": images}
    )

@login_required
def image_ranking(request):
    image_ranking = red.zrange(
        "image_ranking", 0, -1, desc=True
    )[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(
        Image.objects.filter(id__in=image_ranking_ids)
    )
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request, "images/ranking.html",
        {"section": "images", "most_viewed": most_viewed}
        )