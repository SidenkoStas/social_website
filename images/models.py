from email.mime import image
from tabnanny import verbose
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    """Модель для хранения информации об изображении.

    Attributes:
        user: Ссылка на пользователя, создавшего изображение.
        title: Название изображения (максимум 200 символов).
        slug: Уникальный идентификатор для URL (автоматически генерируется, если не указан).
        image: Файл изображения, сохраняемый в директории images/%Y/%m/%d/.
        url: Ссылка на источник изображения (максимум 2000 символов).
        description: Описание изображения (необязательное поле).
        users_like: Множественная связь с пользователями, которые отметили изображение как понравившееся.
        created: Дата и время создания записи (автоматически заполняется).

    Meta:
        Индекс по полю created (по убыванию) для ускорения запросов.
        Запросы автоматически сортируются по дате создания (по убыванию).

    Methods:
        save: Переопределённый метод сохранения, автоматически генерирующий slug из title при его отсутствии.
        __str__: Возвращает строковое представление объекта (название изображения).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(
        upload_to="images/%Y/%m/%d/", verbose_name="Изображение"
        )
    url = models.URLField(max_length=2000)
    description = models.TextField(blank=True, verbose_name="Описание")
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("images:detail", args=(self.id, self.slug))

    def __str__(self):
        return f"{self.title}"
