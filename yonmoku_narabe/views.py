from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Game


def game_list(request):
    """ゲーム一覧"""
    games = Game.objects.all().order_by("-updated_at")
    return render(request, "yonmoku_narabe/game_list.html", {"games": games})


def game_create(request):
    """新しいゲームを作成"""
    game = Game.objects.create()
    game.init_board()
    context = {
        "game": game,
        "board_json": json.dumps(game.board),
    }
    return render(request, "yonmoku_narabe/game.html", context)


def game_detail(request, game_id):
    """ゲーム詳細"""
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game,
        "board_json": json.dumps(game.board),
    }
    return render(request, "yonmoku_narabe/game.html", context)


@require_http_methods(["POST"])
def delete_all_games(request):
    """ゲーム履歴を全削除して一覧に戻す"""
    Game.objects.all().delete()
    return redirect("yonmoku_list")


@require_http_methods(["POST"])
def delete_game(request, game_id):
    """単一ゲームを削除して一覧に戻す"""
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return redirect("yonmoku_list")


@require_http_methods(["POST"])
def move(request, game_id):
    """盤面に石を置く"""
    game = get_object_or_404(Game, id=game_id)

    if game.status == "finished":
        return JsonResponse({"status": "error", "message": "Game is already finished"})

    try:
        data = json.loads(request.body)
        row = data.get("row")
        col = data.get("col")

        if not isinstance(row, int) or not isinstance(col, int):
            return JsonResponse({"status": "error", "message": "Invalid row or col"})

        if not (0 <= row < 8 and 0 <= col < 8):
            return JsonResponse({"status": "error", "message": "Out of bounds"})

        key = f"{row}_{col}"
        if game.board.get(key) is not None:
            return JsonResponse({"status": "error", "message": "Cell already occupied"})

        player = game.current_player
        game.make_move(row, col, player)

        return JsonResponse(
            {
                "status": "success",
                "board": game.board,
                "current_player": game.current_player,
                "game_status": game.status,
                "winner": game.winner,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
def reset_game(request, game_id):
    """ゲームをリセット"""
    game = get_object_or_404(Game, id=game_id)
    game.init_board()

    return JsonResponse(
        {
            "status": "success",
            "board": game.board,
            "current_player": game.current_player,
            "game_status": game.status,
            "winner": game.winner,
        }
    )
