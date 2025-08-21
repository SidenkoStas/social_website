from urllib import response
from django import forms
from django.forms import widgets
from django.core.files.base import ContentFile
from .models import Image, slugify
import requests

class ImageCreateForm(forms.ModelForm):
    """
    Конфигурация формы:
        - `model` = Модель `Image`, к которой привязана форма.
        - `fields` = Поля формы: `title`, `url`, `description`.
        - `widgets` = Скрытый виджет для поля `url`.
    """
    class Meta:
        model = Image
        fields = ("title", "url", "description")
        widgets = {"url": forms.HiddenInput}
    
    def clean_url(self):
        """
        Проверяет валидность URL изображения по расширению файла.
        
        Raises:
            forms.ValidationError: Если URL не содержит допустимое расширение (`.jpg`, `.png`, `.jpeg`).
        
        Returns:
            str: Валидированный URL.
        """
        url = self.cleaned_data["url"]
        valid_extension = (".jpg", ".png", ".jpeg")
        if not url.lower().endswith(valid_extension):
            raise forms.ValidationError(
                "В URL не содержится допустимый формат файла."
                )
        return url
    
    def save(self, force_insert=False, force_update=False, commit = True):
        """
        Переопределённый метод сохранения формы:
            1. Выполняет загрузку изображения по URL.
            2. Сохраняет изображение с именем, сгенерированным на основе заголовка и расширения файла.
        
        Args:
            force_insert (bool): Принудительное вставление объекта в БД.
            force_update (bool): Принудительное обновление объекта в БД.
            commit (bool): Флаг сохранения объекта в БД.
        
        Returns:
            Image: Объект модели `Image` с сохранённым изображением.
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        title = slugify(self.cleaned_data["title"])
        extension = image_url.rspit(".", 1)[-1].lower()
        image_name = f"{title}.{extension}"
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response),
            save=False
        )
        if commit:
            image.save()
        return image