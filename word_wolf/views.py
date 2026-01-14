from django.shortcuts import render
import random
from word_wolf import theme_words

from django.shortcuts import redirect

# Create your views here.


def word_home(request):
    return render(request, "word_wolf/home.html")


def player_name(request):
    if request.method == "POST":
        # フォームからプレイヤー名とウルフ数を取得
        player_names = []
        i = 1
        while f"player_{i}_name" in request.POST:
            name = request.POST.get(f"player_{i}_name")
            if name:
                player_names.append(name)
            i += 1

        wolfcount = request.POST.get("wolfcount", "1")
        talk_theme = request.POST.get("talk_theme")

        # プレイヤー情報をセッションに保存
        request.session["player_names"] = player_names
        request.session["wolf_count"] = int(wolfcount)
        if talk_theme:
            try:
                request.session["theme_category"] = int(talk_theme)
            except ValueError:
                request.session["theme_category"] = 6

        return redirect("assign_roles")

    return render(request, "word_wolf/player_name.html")


def assign_roles(request):
    """ウルフと市民をランダムに割り当て"""
    player_names = request.session.get("player_names", [])
    wolf_count = request.session.get("wolf_count", 1)
    theme_category = request.session.get("theme_category", 6)

    if not player_names:
        from django.shortcuts import redirect

        return redirect("word_home")

    # プレイヤーのリストを作成
    players = [
        {"name": name, "role": None, "theme": "", "voted_for": None, "voted_count": 0}
        for name in player_names
    ]

    # ウルフをランダムに選定（設定されたwolf_countを使用）
    wolf_count = min(wolf_count, len(players))
    wolf_indices = random.sample(range(len(players)), wolf_count)

    for idx in wolf_indices:
        players[idx]["role"] = "wolf"

    for idx, player in enumerate(players):
        if player["role"] is None:
            player["role"] = "citizen"

    # テーマの割り当て（カテゴリからランダムに1組を選ぶ）
    pairs = theme_words.THEME_WORDS.get(theme_category)
    if not pairs:
        # フォールバック: 全カテゴリからランダムに1組選ぶ
        all_pairs = theme_words.all_pairs()
        category, normal_theme, wolf_theme = random.choice(all_pairs)
    else:
        normal_theme, wolf_theme = random.choice(pairs)

    # 各プレイヤーにテーマを付与（ウルフは wolf_theme、それ以外は normal_theme）
    for p in players:
        p["theme"] = wolf_theme if p["role"] == "wolf" else normal_theme

    # セッションに保存
    request.session["players"] = players

    return render(
        request,
        "word_wolf/player_wolf.html",
        {
            "players": players,
        },
    )


def game_start(request):
    return render(request, "word_wolf/game_start.html")


def game_display(request):
    """ゲーム議論画面を表示"""
    players = request.session.get("players", [])

    if not players:
        from django.shortcuts import redirect

        return redirect("word_home")

    # テーマは players に含まれている（assign_roles で付与済み）
    context = {
        "players": players,
        "theme": players[0]["theme"] if players else "",
        "user_role": "citizen",
    }

    return render(request, "word_wolf/game.html", context)


def voting(request):
    players = request.session.get("players", [])
    if not players:
        return redirect("word_home")

    message = None

    if request.method == "POST":
        voter_name = request.POST.get("voter")
        target_name = request.POST.get("target")

        voter_idx = next(
            (i for i, p in enumerate(players) if p["name"] == voter_name), None
        )
        target_idx = next(
            (i for i, p in enumerate(players) if p["name"] == target_name), None
        )

        if voter_idx is None or target_idx is None:
            message = "無効な投票です"
        else:
            # もし既に投票していれば古い投票を取り消す
            prev = players[voter_idx].get("voted_for")
            if prev is not None and 0 <= prev < len(players):
                players[prev]["voted_count"] = max(
                    0, players[prev].get("voted_count", 1) - 1
                )

            players[voter_idx]["voted_for"] = target_idx
            players[target_idx]["voted_count"] = (
                players[target_idx].get("voted_count", 0) + 1
            )

            # 判定: 投票先がウルフかどうか
            is_wolf = players[target_idx]["role"] == "wolf"
            message = (
                f"{target_name} は {'人狼' if is_wolf else '人狼ではありません'}。"
            )

            # セッション更新
            request.session["players"] = players

    return render(
        request, "word_wolf/voting.html", {"players": players, "message": message}
    )


def reveal(request):
    players = request.session.get("players", [])
    if not players:
        return redirect("word_home")

    return render(request, "word_wolf/reveal.html", {"players": players})
