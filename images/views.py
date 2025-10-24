from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from pip._internal import req
from .forms import ImageCreateForm
from .models import Image
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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
    return render(
        request, "images/detail.html", {"section": "images", "image": image}
        )

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})

