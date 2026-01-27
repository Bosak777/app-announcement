// game.js: smooth animations and visual feedback for baseball game
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('actionForm');
    const ball = document.getElementById('ball');
    const resultText = document.getElementById('resultText');
    const scoreboard = document.querySelector('.scoreboard');
    let isAnimating = false;

    if (!form || !ball) return;

    // Add click handlers to all action buttons
    const buttons = form.querySelectorAll('button[name="action"]');
    buttons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            // Prevent multiple rapid clicks
            if (isAnimating) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }

            isAnimating = true;

            // Disable all buttons during animation
            buttons.forEach(b => b.disabled = true);

            // Visual feedback: button press
            btn.classList.add('pressed');
            setTimeout(() => btn.classList.remove('pressed'), 200);

            // Flash scoreboard on action
            if (scoreboard) {
                scoreboard.classList.add('pulse');
                setTimeout(() => scoreboard.classList.remove('pulse'), 600);
            }

            // Show and animate ball
            ball.classList.add('active');
            ball.classList.remove('homerun', 'hit', 'out', 'walk');

            // Delay before adding ball trajectory class
            setTimeout(function () {
                const trajectories = ['homerun', 'hit', 'out', 'walk'];
                const randomTrajectory = trajectories[Math.floor(Math.random() * trajectories.length)];
                ball.classList.add(randomTrajectory);
            }, 200);

            // After animation completes, submit the form
            setTimeout(function () {
                ball.classList.remove('active', 'homerun', 'hit', 'out', 'walk');

                // Re-enable buttons and reset state
                buttons.forEach(b => b.disabled = false);
                isAnimating = false;

                // Submit form to get real result
                form.submit();
            }, 1200);
        });
    });

    // Highlight result with color based on outcome (on page load)
    if (resultText && resultText.textContent.trim()) {
        const text = resultText.textContent;
        resultText.parentElement.classList.add('result-show');

        // Determine result type and add appropriate class
        if (text.includes('ホームラン') || text.includes('ヒット') || text.includes('四球') || text.includes('成功')) {
            resultText.parentElement.classList.add('success');
        } else if (text.includes('三振') || text.includes('凡打') || text.includes('失敗') || text.includes('見逃し三振')) {
            resultText.parentElement.classList.add('fail');
        } else if (text.includes('見逃し') || text.includes('次の球')) {
            resultText.parentElement.classList.add('neutral');
        }

        // Animate text
        resultText.style.animation = 'resultPop 0.5s ease-out';
    }
});

});


