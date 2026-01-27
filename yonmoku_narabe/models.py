from django.db import models


class Game(models.Model):
    """四目並べゲームモデル"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("finished", "Finished"),
    ]

    board = models.JSONField(default=dict)  # 8x8のボード状態を保存
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    winner = models.CharField(
        max_length=10, null=True, blank=True
    )  # 'black', 'white', 'draw'
    current_player = models.CharField(
        max_length=10, default="black"
    )  # 現在のプレイヤー
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id} - {self.status}"

    def init_board(self):
        """ボードを初期化（8x8）"""
        # ボード状態を辞書として保存
        self.board = {f"{row}_{col}": None for row in range(8) for col in range(8)}
        self.status = "active"
        self.current_player = "black"
        self.winner = None
        self.save()

    def make_move(self, row, col, player):
        """石を置く"""
        key = f"{row}_{col}"
        if self.board.get(key) is not None:
            return False

        self.board[key] = player
        self.current_player = "white" if player == "black" else "black"

        if self.check_winner(row, col, player):
            self.winner = player
            self.status = "finished"
        elif self.is_board_full():
            self.winner = "draw"
            self.status = "finished"

        self.save()
        return True

    def check_winner(self, row, col, player):
        """4目並べがあるか確認"""
        directions = [
            (0, 1),  # 横
            (1, 0),  # 縦
            (1, 1),  # 斜め（右下）
            (1, -1),  # 斜め（左下）
        ]

        for dr, dc in directions:
            count = 1
            # 正の方向
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board.get(f"{r}_{c}") == player:
                count += 1
                r += dr
                c += dc

            # 負の方向
            r, c = row - dr, col - dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board.get(f"{r}_{c}") == player:
                count += 1
                r -= dr
                c -= dc

            if count >= 4:
                return True

        return False

    def is_board_full(self):
        """ボードが満杯か確認"""
        return all(v is not None for v in self.board.values())
