from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'
    verbose_name = "Изображения"

    def ready(self):
        """
        Подключение сигналов к приложению.
        """
        import images.signals