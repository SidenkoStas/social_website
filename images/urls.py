from django.urls import path
from images import views

app_name = "images"

urlpatterns = [
    path("create/", views.create_image, name="create"),
]
