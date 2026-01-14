const cards = document.querySelectorAll(".card");

// ゲーム開始時刻をセッションストレージに保存
if (!sessionStorage.getItem('gameStartTime')) {
    sessionStorage.setItem('gameStartTime', Date.now());
}

// 難易度を判定して保存
function detectDifficulty() {
    const cardCount = cards.length;
    if (cardCount === 20) return 'easy';
    if (cardCount === 36) return 'normal';
    if (cardCount === 48) return 'hard';
    return 'unknown';
}

sessionStorage.setItem('gameDifficulty', detectDifficulty());

// カードをランダムに配置
cards.forEach(card => {
    const randomRotation = Math.random() * 10 - 5; // -5度～+5度のランダムな回転
    card.style.transform = `rotate(${randomRotation}deg)`;
});

let firstCard = null;
let secondCard = null;
let lockBoard = false; // true の間は他のカードをクリックできない

function resetTurn() {
    firstCard = null;
    secondCard = null;
    lockBoard = false;
}

// ゲーム完了判定
function checkGameClear() {
    const matchedCards = document.querySelectorAll(".card.matched");
    if (matchedCards.length === cards.length) {
        // すべてのカードが揃った
        setTimeout(() => {
            window.location.href = "/app/game_clear/";
        }, 500);
    }
}

cards.forEach(card => {
    card.addEventListener("click", function (e) {
        if (lockBoard) return; // 解決中はクリック無効
        if (this.classList.contains('matched')) return; // 既に揃っているカードは無視
        // 同じカードを2回連続で選ぶのを防ぐ
        if (this === firstCard) return;

        this.classList.add("is-flipped");

        // クリックされたカードの front 画像を取得（ログ用）
        const cardInner = this.querySelector(".card-inner");
        const frontImg = this.querySelector(".front");
        if (frontImg) console.log("front:", frontImg.src);

        if (!firstCard) {
            // 1枚目選択
            firstCard = this;
            return;
        }

        // 2枚目選択
        secondCard = this;
        // 2枚選択されたのでボードをロックして他を選べなくする
        lockBoard = true;

        const firstSrc = firstCard.querySelector('.front')?.src;
        const secondSrc = secondCard.querySelector('.front')?.src;

        const handleMatch = () => {
            // 揃った場合: matched クラスを付与してクリック不可にする
            firstCard.classList.add('matched');
            secondCard.classList.add('matched');
            firstCard.style.pointerEvents = 'none';
            secondCard.style.pointerEvents = 'none';

            // マッチしたカードだけを光らせる（隣のカードは光らせない）
            firstCard.classList.add('glow');
            secondCard.classList.add('glow');

            // リセット（ハイライトは消さずに保持）
            resetTurn();
            
            // ゲーム完了判定
            checkGameClear();
        };

        const handleMismatch = () => {
            // 外れた場合: 1.5秒待ってから裏返す
            setTimeout(() => {
                firstCard.classList.remove('is-flipped');
                secondCard.classList.remove('is-flipped');
                resetTurn();
            }, 1500);
        };

        if (firstSrc && secondSrc && firstSrc === secondSrc) {
            handleMatch();
        } else {
            handleMismatch();
        }
    });
});