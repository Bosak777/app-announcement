from django.urls import path
from . import views

urlpatterns = [
    path("", views.app_game, name="app_game"),
    path("easy_game/", views.easy_game, name="easy_game"),
    path("normal_game/", views.normal_game, name="normal_game"),
    path("hard_game/", views.hard_game, name="hard_game"),
    path("game_clear/", views.game_clear, name="game_clear"),
]
