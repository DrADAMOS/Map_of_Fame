const Animations = {
    click: (el) => {
        el.style.transform = 'scale(0.95)';
        setTimeout(() => { el.style.transform = 'scale(1)'; }, 100);
    },

    fadeIn: (id, display = 'flex') => {
        const el = document.getElementById(id);
        if (!el) return;
        el.style.display = display;
        el.style.opacity = '0';
        el.style.transform = 'scale(0.95) translateY(10px)';
        el.style.pointerEvents = 'auto';

        setTimeout(() => {
            el.style.transition = 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            el.style.opacity = '1';
            el.style.transform = 'scale(1) translateY(0)';
        }, 50);
    },

    fadeOut: (id) => {
        console.log("Fading out element:", id);
        const el = document.getElementById(id);
        if (!el) {
            console.error("Element not found for fadeOut:", id);
            return;
        }
        el.style.transition = 'all 0.5s ease-in';
        el.style.opacity = '0';
        el.style.transform = 'scale(1.05)';
        el.style.pointerEvents = 'none'; // Prevent clicks while fading
        setTimeout(() => {
            el.style.display = 'none';
            console.log("Element hidden:", id);
        }, 500);
    },

    scoreRoll: (target) => {
        const el = document.getElementById('scoreTxt');
        const start = parseInt(el.textContent) || 0;
        const duration = 1200;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOutExpo = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
            const current = Math.floor(start + (target - start) * easeOutExpo(progress));

            el.textContent = current;
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    },

    shake: (id) => {
        const el = document.getElementById(id);
        el.classList.add('shake-anim');
        setTimeout(() => el.classList.remove('shake-anim'), 500);
    },

    successGlow: (el) => {
        el.style.boxShadow = '0 0 20px var(--success)';
        setTimeout(() => { el.style.boxShadow = 'none'; }, 1000);
    }
};
