from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("yonmoku_title/", views.yonmoku_title, name="yonmoku_title"),
]
