from django.db import models
from django.conf import settings

class Profile(models.Model):
    """
    Модель для дополнителтной минформации о пользователе. Расширяет существующую
    модель пользователя.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name="Пользователь"
        )
    date_of_birth = models.DateField(
        blank=True, null=True,verbose_name="Дата рождения"
        )
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, verbose_name="Фото"
    )

    def __str__(self):
        return f"Профиль {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
