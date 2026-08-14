const Music = (() => {
    let ctx = null, masterGain = null;
    let isPlaying = false;
    const SCALE = [146.83, 174.61, 220.00, 293.66, 349.23];

    function init() {
        if (ctx) return;
        try {
            ctx = new (window.AudioContext || window.webkitAudioContext)();
            masterGain = ctx.createGain();
            masterGain.gain.value = 0.9;
            masterGain.connect(ctx.destination);
        } catch(e) { console.error(e); }
    }

    let playTimeout = null;

    function playLoop() {
        if (!isPlaying || !ctx) return;
        if (ctx.state === 'suspended') ctx.resume();

        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.value = SCALE[Math.floor(Math.random() * SCALE.length)];

        const now = ctx.currentTime;
        g.gain.setValueAtTime(0, now);
        g.gain.linearRampToValueAtTime(0.4, now + 1);
        g.gain.exponentialRampToValueAtTime(0.001, now + 5);

        osc.connect(g); g.connect(masterGain);
        osc.start(now); osc.stop(now + 5);

        if(playTimeout) clearTimeout(playTimeout);
        playTimeout = setTimeout(playLoop, 3500 + Math.random() * 2000);
    }

    function updateUI() {
        const btn = document.getElementById('musicBtn');
        if (!btn) return;
        if(isPlaying) {
            btn.style.color = '#f0a500';
            btn.innerHTML = `<div class="eq-container"><div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div></div>`;
        } else {
            btn.style.color = 'gray';
            btn.innerHTML = `<i class="fas fa-music"></i>`;
        }
    }

    return {
        unlock: () => {
            if(!ctx) init();
            if(ctx && ctx.state === 'suspended') ctx.resume();
        },
        toggle: () => {
            if(!ctx) init();
            if(ctx && ctx.state === 'suspended') {
                ctx.resume().then(() => {
                    isPlaying = !isPlaying;
                    if(isPlaying) playLoop();
                    updateUI();
                });
            } else {
                isPlaying = !isPlaying;
                if(isPlaying) playLoop();
                updateUI();
            }
        },
        sfx: (f) => {
            if(!ctx) init();
            if(ctx && ctx.state === 'suspended') ctx.resume();
            const o = ctx.createOscillator(); const g = ctx.createGain();
            o.type = 'sine'; o.frequency.value = f;
            g.gain.setValueAtTime(0.3, ctx.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
            o.connect(g); g.connect(ctx.destination);
            o.start(); o.stop(ctx.currentTime + 0.3);
        },
        win: () => {
            if(!ctx) init();
            if(ctx && ctx.state === 'suspended') ctx.resume();
            const now = ctx.currentTime;
            const notes = [523.25, 659.25, 783.99, 1046.50];
            notes.forEach((f, i) => {
                const o = ctx.createOscillator();
                const g = ctx.createGain();
                o.type = 'triangle';
                o.frequency.value = f;
                g.gain.setValueAtTime(0, now + i * 0.1);
                g.gain.linearRampToValueAtTime(0.2, now + i * 0.1 + 0.05);
                g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.4);
                o.connect(g); g.connect(ctx.destination);
                o.start(now + i * 0.1); o.stop(now + i * 0.1 + 0.4);
            });
        }
    };
})();
