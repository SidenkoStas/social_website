from django.urls import path
from images import views

app_name = "images"

urlpatterns = [
    path("", views.image_list, name="list"),
    path("create/", views.create_image, name="create"),
    path("detail/<int:id>/<str:slug>/", views.image_detail, name="detail"),
    path("like/", views.image_like, name="like"),
    path("ranking/", views.image_ranking, name="ranking"),
]
