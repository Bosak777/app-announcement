from django.shortcuts import render
import os
import random

# Create your views here.


def easy_game(request):
    # 静的カード画像フォルダのパス
    card_dir = "card_game/static/cards"

    # cardBack 以外のpngファイル（トランプ画像）だけ取得
    all_cards = [
        f for f in os.listdir(card_dir) if f.endswith(".png") and "back" not in f
    ]

    # 10種類ランダムに選ぶ
    selected = random.sample(all_cards, 10)

    # 各かーどを2枚にして20枚にする
    cards = []
    for i, img in enumerate(selected):
        cards.append({"img": img, "num": i})
        cards.append({"img": img, "num": i})

    # カードをシャッフル
    random.shuffle(cards)

    return render(request, "card_game/easy_game.html", {"cards": cards})


def app_game(request):
    return render(request, "card_game/app_game.html")


def normal_game(request):
    # 静的カード画像フォルダのパス
    card_dir = "card_game/static/cards"
    # cardBck 以外のpngファイル（トランプ画像）だけ取得
    all_cards = [
        f for f in os.listdir(card_dir) if f.endswith(".png") and "back" not in f
    ]
    # 18種類ランダムに選ぶ
    selected = random.sample(all_cards, 18)

    # 各カードを2枚にして36枚にする
    cards = selected * 2

    return render(request, "card_game/normal_game.html", {"cards": cards})


def hard_game(request):
    # 静的カード画像フォルダのパス
    card_dir = "card_game/static/cards"
    # cardBck 以外のpngファイル（トランプ画像）だけ取得
    all_cards = [
        f for f in os.listdir(card_dir) if f.endswith(".png") and "back" not in f
    ]
    # 26種類ランダムに選ぶ
    selected = random.sample(all_cards, 26)

    # 各カードを2枚にして52枚にする
    cards = selected * 2

    return render(request, "card_game/hard_game.html", {"cards": cards})


def game_clear(request):
    return render(request, "card_game/game_clear.html")
