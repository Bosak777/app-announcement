from django.urls import path
from . import views

urlpatterns = [
    path("", views.word_home, name="word_home"),
    path("player_name/", views.player_name, name="player_name"),
    path("assign_roles/", views.assign_roles, name="assign_roles"),
    path("game_start/", views.game_start, name="game_start"),
    path("game/", views.game_display, name="game_display"),
    path("vote/", views.voting, name="voting"),
    path("reveal/", views.reveal, name="reveal"),
]
