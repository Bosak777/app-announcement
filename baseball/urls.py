from django.urls import path
from . import views

app_name = "baseball"

# '' -> タイトル画面、'play/' -> ゲーム画面
urlpatterns = [
    path("", views.title, name="title"),
    path("play/", views.index, name="index"),
]
