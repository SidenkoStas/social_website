from django.urls import path
from images import views

app_name = "images"

urlpatterns = [
    path("create/", views.create_image, name="create"),
    path("detail/<int:id>/<slug:slug>/", views.image_detail, name="detail"),
]
