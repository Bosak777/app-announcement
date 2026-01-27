class YonmokuGame {
    constructor(gameId, initialBoard, initialStatus, initialCurrentPlayer, initialWinner) {
        this.gameId = gameId;
        this.board = initialBoard;
        this.status = initialStatus;
        this.currentPlayer = initialCurrentPlayer;
        this.winner = initialWinner;
        this.boardElement = document.getElementById('gameBoard');
        this.resetBtn = document.getElementById('resetBtn');

        this.init();
        this.attachEventListeners();
    }

    init() {
        this.renderBoard();
        this.updateUI();
    }

    renderBoard() {
        this.boardElement.innerHTML = '';
        console.log('ボード:', this.board);
        console.log('ボード型:', typeof this.board);

        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = row;
                cell.dataset.col = col;

                const key = `${row}_${col}`;
                const stone = this.board[key];
                if (stone) {
                    const stoneElement = document.createElement('div');
                    stoneElement.className = `stone ${stone}`;
                    cell.appendChild(stoneElement);
                }

                cell.addEventListener('click', () => this.makeMove(row, col));
                this.boardElement.appendChild(cell);
            }
        }
        console.log('ボード生成完了。セル数:', this.boardElement.children.length);
    }

    async makeMove(row, col) {
        if (this.status === 'finished') {
            alert('ゲームは終了しています');
            return;
        }

        const key = `${row}_${col}`;
        if (this.board[key] !== null && this.board[key] !== undefined) {
            alert('そのマスには既に石が置かれています');
            return;
        }

        try {
            const response = await fetch(`/yonmoku_narabe/${this.gameId}/move/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ row, col })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.board = data.board;
                this.currentPlayer = data.current_player;
                this.status = data.game_status;
                this.winner = data.winner;

                this.renderBoard();
                this.updateUI();

                if (this.status === 'finished') {
                    this.showGameResult();
                }
            } else {
                alert('エラー: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('リクエスト中にエラーが発生しました');
        }
    }

    async resetGame() {
        try {
            const response = await fetch(`/yonmoku_narabe/${this.gameId}/reset/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.board = data.board;
                this.currentPlayer = data.current_player;
                this.status = data.game_status;
                this.winner = data.winner;

                this.renderBoard();
                this.updateUI();
            } else {
                alert('エラー: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('リセット中にエラーが発生しました');
        }
    }

    updateUI() {
        document.getElementById('currentPlayer').textContent = this.currentPlayer;
        document.getElementById('currentPlayer').dataset.player = this.currentPlayer;

        const gameStatusElement = document.getElementById('gameStatus');
        gameStatusElement.textContent = this.status === 'finished' ? '終了' : 'プレイ中';
        gameStatusElement.className = `status ${this.status}`;

        const winnerInfo = document.getElementById('winnerInfo');
        if (this.winner) {
            winnerInfo.style.display = 'block';
            document.getElementById('winner').textContent = this.getWinnerText();
        } else {
            winnerInfo.style.display = 'none';
        }
    }

    getWinnerText() {
        if (this.winner === 'draw') {
            return '引き分け';
        } else if (this.winner === 'black') {
            return '黒（先手）';
        } else if (this.winner === 'white') {
            return '白（後手）';
        }
        return '';
    }

    showGameResult() {
        const message = this.winner === 'draw'
            ? 'ゲーム終了：引き分けです'
            : `ゲーム終了：${this.getWinnerText()}の勝利です！`;
        alert(message);
    }

    attachEventListeners() {
        this.resetBtn.addEventListener('click', () => {
            if (confirm('ゲームをリセットしますか？')) {
                this.resetGame();
            }
        });
    }

    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// ゲーム初期化
document.addEventListener('DOMContentLoaded', () => {
    new YonmokuGame(gameId, initialBoard, initialStatus, initialCurrentPlayer, initialWinner);
});
