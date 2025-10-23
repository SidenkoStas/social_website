from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from .models import Image
from django.shortcuts import get_object_or_404

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
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request, "images/detail.html", {"section": "images", "image": image}
        )
