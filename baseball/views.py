from django.shortcuts import render, redirect
import random


def title(request):
    """タイトル画面を表示するシンプルなビュー"""
    return render(request, "baseball/title.html")


def _new_game():
    return {
        "scores": {"1": 0, "2": 0},
        "current": 1,
        "outs": 0,
        "strikes": 0,
        "balls": 0,
        "bases": [False, False, False],
        "message": "ゲーム開始！プレイヤー1の攻撃です。",
        "finished": False,
        "half_finished": {"1": False, "2": False},
    }


def _advance_on_hit(bases):
    """シンプルにランナーを1ベース進めて、ホームを越えたランナーを返す"""
    runs = 0
    if bases[2]:
        runs += 1
    bases[2] = bases[1]
    bases[1] = bases[0]
    bases[0] = True
    return runs, bases


def _walk(bases):
    runs = 0
    if not bases[0]:
        bases[0] = True
    else:
        if bases[1]:
            if bases[2]:
                runs += 1
            bases[2] = bases[1]
        bases[1] = bases[0]
        bases[0] = True
    return runs, bases


def index(request):
    """ゲーム画面：セッションにゲームを保持し、2人交互でプレイする"""
    session = request.session
    game = session.get("baseball_game")

    if game is None or request.GET.get("new") == "1":
        game = _new_game()
        session["baseball_game"] = game

    choices = {"strong": "強振", "meet": "ミート", "bunt": "バント", "take": "見送る"}

    if request.method == "POST" and not game.get("finished"):
        action = request.POST.get("action", "").strip()
        player = str(game["current"])
        message = ""
        runs_scored = 0

        if action == "strong":
            # 強振：ストライク60%、ボール40%
            outcome = random.choices(["ストライク", "ボール"], weights=[0.60, 0.40])[0]
            if outcome == "ストライク":
                game["strikes"] += 1
                message = f"💥強振 → ストライク！（{game['strikes']}-{game['balls']}）"
                if game["strikes"] >= 3:
                    game["outs"] += 1
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"💥強振 → ストライク！3ストライク アウト！"
            else:
                game["balls"] += 1
                message = f"💥強振 → ボール（{game['strikes']}-{game['balls']}）"
                if game["balls"] >= 4:
                    r, game["bases"] = _walk(game["bases"])
                    runs_scored += r
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"💥強振 → ボール！4ボール フォアボール！"

        elif action == "meet":
            # ミート：ストライク75%、ボール25%
            outcome = random.choices(["ストライク", "ボール"], weights=[0.75, 0.25])[0]
            if outcome == "ストライク":
                game["strikes"] += 1
                # ストライク時にヒット判定（50%）
                if random.random() < 0.50:
                    r, game["bases"] = _advance_on_hit(game["bases"])
                    runs_scored += r
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"✅ミート → ストライク ヒット！（{game['strikes']}-{game['balls']}）"
                else:
                    message = (
                        f"✅ミート → ストライク！（{game['strikes']}-{game['balls']}）"
                    )
                    if game["strikes"] >= 3:
                        game["outs"] += 1
                        game["strikes"] = 0
                        game["balls"] = 0
                        message = f"✅ミート → ストライク！3ストライク アウト！"
            else:
                game["balls"] += 1
                message = f"✅ミート → ボール（{game['strikes']}-{game['balls']}）"
                if game["balls"] >= 4:
                    r, game["bases"] = _walk(game["bases"])
                    runs_scored += r
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"✅ミート → ボール！4ボール フォアボール！"

        elif action == "bunt":
            # バント：ストライク85%、ボール15%
            outcome = random.choices(["ストライク", "ボール"], weights=[0.85, 0.15])[0]
            if outcome == "ストライク":
                game["strikes"] += 1
                # バント時に成功判定（70%）
                if random.random() < 0.70:
                    if game["bases"][2]:
                        runs_scored += 1
                        game["bases"][2] = False
                    game["bases"][2] = game["bases"][1]
                    game["bases"][1] = game["bases"][0]
                    game["bases"][0] = True
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"🎯バント → ストライク 成功！"
                else:
                    message = (
                        f"🎯バント → ストライク！（{game['strikes']}-{game['balls']}）"
                    )
                    if game["strikes"] >= 3:
                        game["outs"] += 1
                        game["strikes"] = 0
                        game["balls"] = 0
                        message = f"🎯バント → ストライク！3ストライク アウト！"
            else:
                game["balls"] += 1
                message = f"🎯バント → ボール（{game['strikes']}-{game['balls']}）"
                if game["balls"] >= 4:
                    r, game["bases"] = _walk(game["bases"])
                    runs_scored += r
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"🎯バント → ボール！4ボール フォアボール！"

        elif action == "take":
            # 見送る：ストライク20%、ボール80%
            outcome = random.choices(["ストライク", "ボール"], weights=[0.20, 0.80])[0]
            if outcome == "ストライク":
                game["strikes"] += 1
                message = f"➡見送る → ストライク！（{game['strikes']}-{game['balls']}）"
                if game["strikes"] >= 3:
                    game["outs"] += 1
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"➡見送る → ストライク！3ストライク アウト！"
            else:
                game["balls"] += 1
                message = f"➡見送る → ボール（{game['strikes']}-{game['balls']}）"
                if game["balls"] >= 4:
                    r, game["bases"] = _walk(game["bases"])
                    runs_scored += r
                    game["strikes"] = 0
                    game["balls"] = 0
                    message = f"➡見送る → ボール！4ボール フォアボール！"

        else:
            if action:
                message = f"不正な選択です。(受け取り値: {action})"
            else:
                message = "アクションが選択されていません。"

        if runs_scored:
            game["scores"][player] += runs_scored

        if game["outs"] >= 3:
            game["half_finished"][player] = True
            game["outs"] = 0
            game["strikes"] = 0
            game["balls"] = 0
            game["bases"] = [False, False, False]
            if not game["half_finished"]["1"] or not game["half_finished"]["2"]:
                game["current"] = 2 if game["current"] == 1 else 1
                message += f" 3アウト。プレイヤー{game['current']}の攻撃に移ります。"
            else:
                game["finished"] = True
                if game["scores"]["1"] > game["scores"]["2"]:
                    message += f" 試合終了。プレイヤー1の勝ち（{game['scores']['1']} - {game['scores']['2']}）"
                elif game["scores"]["1"] < game["scores"]["2"]:
                    message += f" 試合終了。プレイヤー2の勝ち（{game['scores']['2']} - {game['scores']['1']}）"
                else:
                    message += f" 試合終了。引き分け（{game['scores']['1']} - {game['scores']['2']}）"

        game["message"] = message
        session["baseball_game"] = game
        session.modified = True

        return redirect("/baseball/play/")

    context = {
        "result": game.get("message"),
        "scores": game.get("scores"),
        "score1": game.get("scores").get("1"),
        "score2": game.get("scores").get("2"),
        "current": game.get("current"),
        "outs": game.get("outs"),
        "strikes": game.get("strikes", 0),
        "balls": game.get("balls", 0),
        "bases": game.get("bases"),
        "finished": game.get("finished"),
        "choices": choices,
        "strong_done": False,
        "meet_done": False,
        "bunt_done": False,
        "take_done": False,
    }
    return render(request, "baseball/index.html", context)
