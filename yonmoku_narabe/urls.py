from django.urls import path
from . import views

app_name = "yonmoku_narabe"

urlpatterns = [
    path("", views.game_list, name="yonmoku_list"),
    path("new/", views.game_create, name="yonmoku_create"),
    path("<int:game_id>/", views.game_detail, name="yonmoku_detail"),
    path("<int:game_id>/move/", views.move, name="yonmoku_move"),
    path("<int:game_id>/reset/", views.reset_game, name="yonmoku_reset"),
    path("<int:game_id>/delete/", views.delete_game, name="yonmoku_delete"),
    path("delete_all/", views.delete_all_games, name="yonmoku_delete_all"),
]
