const cards = document.querySelectorAll(".card");

// ゲームページ以外では処理しない
if (cards.length) {
    const playerForm = document.getElementById("player-form");
    const playerInputsWrapper = document.getElementById("player-inputs");
    const addPlayerButton = document.getElementById("add-player");
    const scoreboard = document.getElementById("scoreboard");
    const scoreList = document.getElementById("score-list");
    const turnMessage = document.getElementById("turn-message");
    const resultOverlay = document.getElementById("result-overlay");
    const rankingList = document.getElementById("ranking-list");
    const resultTime = document.getElementById("result-time");
    const resultDifficulty = document.getElementById("result-difficulty");
    const retryButton = document.getElementById("retry-button");
    const MAX_PLAYERS = 4;

    let firstCard = null;
    let secondCard = null;
    let lockBoard = true; // ゲーム開始まではロック
    let gameStarted = false;
    let gameFinished = false;
    let players = [];
    let currentPlayerIndex = 0;
    let matchedPairs = 0;
    const totalPairs = cards.length / 2;

    // 難易度を判定して保存
    function detectDifficulty() {
        const cardCount = cards.length;
        if (cardCount === 20) return "easy";
        if (cardCount === 36) return "normal";
        if (cardCount === 48) return "hard";
        return "unknown";
    }

    sessionStorage.setItem("gameDifficulty", detectDifficulty());

    // カードをランダムに配置
    cards.forEach(card => {
        const randomRotation = Math.random() * 10 - 5; // -5度～+5度のランダムな回転
        card.style.transform = `rotate(${randomRotation}deg)`;
    });

    function resetTurn() {
        firstCard = null;
        secondCard = null;
        lockBoard = false;
    }

    function createPlayerInput(index) {
        const input = document.createElement("input");
        input.className = "player-name-input";
        input.type = "text";
        input.placeholder = `プレイヤー${index}`;
        input.setAttribute("aria-label", `プレイヤー${index}の名前`);
        return input;
    }

    function syncAddButtonState() {
        if (!addPlayerButton || !playerInputsWrapper) return;
        const count = playerInputsWrapper.querySelectorAll(".player-name-input").length;
        addPlayerButton.disabled = count >= MAX_PLAYERS;
    }

    function readPlayersFromInputs() {
        if (!playerInputsWrapper) return [];
        const inputs = Array.from(playerInputsWrapper.querySelectorAll(".player-name-input"));
        const names = inputs
            .map((input, idx) => input.value.trim() || `プレイヤー${idx + 1}`)
            .filter(Boolean)
            .slice(0, MAX_PLAYERS);
        return names.map(name => ({ name, score: 0 }));
    }

    function updateScoreboard() {
        if (!scoreList || !players.length) return;
        scoreList.innerHTML = "";
        players.forEach((player, idx) => {
            const row = document.createElement("li");
            row.className = idx === currentPlayerIndex ? "score-row active" : "score-row";

            const nameSpan = document.createElement("span");
            nameSpan.className = "player-name";
            nameSpan.textContent = player.name;

            const scoreSpan = document.createElement("span");
            scoreSpan.className = "player-score";
            scoreSpan.textContent = `${player.score} ペア`;

            row.appendChild(nameSpan);
            row.appendChild(scoreSpan);
            scoreList.appendChild(row);
        });

        if (turnMessage && players[currentPlayerIndex]) {
            turnMessage.textContent = `${players[currentPlayerIndex].name} の番です`;
        }
    }

    function advancePlayer() {
        if (!players.length) return;
        currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
        updateScoreboard();
    }

    function formatElapsedTime() {
        const startTime = sessionStorage.getItem("gameStartTime");
        if (!startTime) return "--";
        const elapsedSeconds = Math.floor((Date.now() - parseInt(startTime, 10)) / 1000);
        const minutes = Math.floor(elapsedSeconds / 60);
        const seconds = elapsedSeconds % 60;
        return `${minutes}分${seconds}秒`;
    }

    function showResults() {
        if (!resultOverlay || !rankingList) return;
        const ranking = [...players].sort((a, b) => b.score - a.score);
        rankingList.innerHTML = "";
        ranking.forEach((player, idx) => {
            const li = document.createElement("li");
            li.innerHTML = `<span class="rank">${idx + 1}位</span><span class="rank-name">${player.name}</span><span class="rank-score">${player.score} ペア</span>`;
            rankingList.appendChild(li);
        });

        if (resultDifficulty) {
            const diffLabel = {
                easy: "簡単",
                normal: "普通",
                hard: "難しい",
            }[detectDifficulty()] || "-";
            resultDifficulty.textContent = diffLabel;
        }

        if (resultTime) {
            resultTime.textContent = formatElapsedTime();
        }

        resultOverlay.classList.remove("hidden");
        document.body.classList.add("no-scroll");

        // 片付け
        sessionStorage.removeItem("gameStartTime");
    }

    function checkGameClear() {
        if (matchedPairs === totalPairs) {
            gameFinished = true;
            lockBoard = true;
            setTimeout(showResults, 400);
        }
    }

    function startGame() {
        players = readPlayersFromInputs();
        if (!players.length) {
            alert("プレイヤーを1人以上入力してください");
            return;
        }

        gameStarted = true;
        lockBoard = false;
        sessionStorage.setItem("gameStartTime", Date.now());

        if (playerInputsWrapper) {
            playerInputsWrapper.querySelectorAll("input").forEach(input => {
                input.disabled = true;
            });
        }

        if (addPlayerButton) {
            addPlayerButton.disabled = true;
        }

        if (scoreboard) {
            scoreboard.classList.remove("hidden");
        }

        if (playerForm) {
            playerForm.classList.add("form-locked");
        }

        updateScoreboard();
    }

    // イベント: プレイヤー追加
    addPlayerButton?.addEventListener("click", () => {
        if (!playerInputsWrapper) return;
        const currentCount = playerInputsWrapper.querySelectorAll(".player-name-input").length;
        if (currentCount >= MAX_PLAYERS) return;
        playerInputsWrapper.appendChild(createPlayerInput(currentCount + 1));
        syncAddButtonState();
    });

    // イベント: ゲーム開始
    playerForm?.addEventListener("submit", event => {
        event.preventDefault();
        if (gameStarted) return;
        startGame();
    });

    // リトライ
    retryButton?.addEventListener("click", () => {
        window.location.reload();
    });

    // カードクリックイベント
    cards.forEach(card => {
        card.addEventListener("click", function () {
            if (!gameStarted || gameFinished) return;
            if (lockBoard) return; // 解決中はクリック無効
            if (this.classList.contains("matched")) return; // 既に揃っているカードは無視
            if (this === firstCard) return; // 同じカードを2回連続で選ぶのを防ぐ

            this.classList.add("is-flipped");

            const firstSrc = firstCard?.querySelector(".front")?.src;
            const secondSrc = this.querySelector(".front")?.src;

            if (!firstCard) {
                // 1枚目選択
                firstCard = this;
                return;
            }

            // 2枚目選択
            secondCard = this;
            lockBoard = true; // 他のカードを選べなくする

            const handleMatch = () => {
                firstCard.classList.add("matched");
                secondCard.classList.add("matched");
                firstCard.style.pointerEvents = "none";
                secondCard.style.pointerEvents = "none";

                firstCard.classList.add("glow");
                secondCard.classList.add("glow");

                // スコア加算（同じプレイヤーが続けてめくれる）
                if (players[currentPlayerIndex]) {
                    players[currentPlayerIndex].score += 1;
                }
                matchedPairs += 1;
                updateScoreboard();

                resetTurn();
                checkGameClear();
            };

            const handleMismatch = () => {
                setTimeout(() => {
                    firstCard.classList.remove("is-flipped");
                    secondCard.classList.remove("is-flipped");
                    resetTurn();
                    advancePlayer();
                }, 1200);
            };

            if (firstSrc && secondSrc && firstSrc === secondSrc) {
                handleMatch();
            } else {
                handleMismatch();
            }
        });
    });

    // 初期状態で追加ボタンの活性/非活性を整える
    syncAddButtonState();
}
