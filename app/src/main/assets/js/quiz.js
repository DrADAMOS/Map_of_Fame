const ALL = ALL_DATA;

let curQ = [], idx = 0, score = 0, currentLevel = 'easy', TOTAL_Q = 10, currentMode = 'all';
let timerInterval, timeLeft, hinted = false, locked = false;

function setMode(m, btn) {
    Utils.vibrate(20);
    Music.sfx(600);
    currentMode = m;
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    Animations.click(btn);
}

function exitToHome() {
    Utils.vibrate(30);
    Music.sfx(600);
    Animations.fadeIn('exitModal');
}

function confirmExit(yes) {
    Utils.vibrate(20);
    Music.sfx(600);
    Animations.fadeOut('exitModal');
    if (yes) {
        clearInterval(timerInterval);
        if (window.Android && Android.showBanner) Android.showBanner();
        document.getElementById('hud-bar').style.display = 'none';
        document.getElementById('game-ui').style.display = 'none';
        Animations.fadeIn('startScreen');
        if (typeof map !== 'undefined' && map) map.setView([20, 10], 2);
    }
}

function exitToHomeDirect() {
    Utils.vibrate(30);
    if (window.Android && Android.showBanner) Android.showBanner();
    Music.sfx(600);
    document.getElementById('endScreen').style.display = 'none';
    Animations.fadeIn('startScreen');
    if (map) map.setView([20, 10], 2);
}

function startGame(lv) {
    console.log("Starting game level:", lv);
    if (window.Android && Android.hideBanner) Android.hideBanner();
    AchievementEvents.emit('game_started', { level: lv });
    try {
        Utils.vibrate(40);
        Music.sfx(800);
        Music.unlock();

        if (typeof initMap === 'function') initMap();

        currentLevel = lv; idx = 0; score = 0;
        const qSelect = document.getElementById('qCountSelect');
        if (!qSelect) throw new Error("qCountSelect not found");

        TOTAL_Q = parseInt(qSelect.value);
        console.log("Total questions selected:", TOTAL_Q);

        let pool = currentMode === 'all' ? ALL : ALL.filter(x => x.mode === currentMode);
        if (!pool || pool.length === 0) {
            console.warn("Pool is empty for mode:", currentMode);
            pool = ALL;
        }

        curQ = Utils.shuffle(pool).slice(0, Math.min(TOTAL_Q, pool.length));
        TOTAL_Q = curQ.length;
        console.log("Quiz started with", TOTAL_Q, "questions");

        Animations.fadeOut('startScreen');
        setTimeout(() => {
            document.getElementById('hud-bar').style.display = 'flex';
            document.getElementById('game-ui').style.display = 'flex';
            if (map) map.invalidateSize();
            showQ();
        }, 500);
    } catch (e) {
        console.error("Failed to start game:", e);
    }
}

function showQ() {
    if (idx >= TOTAL_Q) { endGame(); return; }
    locked = false; hinted = false;
    const p = curQ[idx];
    const t = I18N[currentLang];
    document.getElementById('qCounter').textContent = `${idx + 1} / ${TOTAL_Q}`;

    document.getElementById('birthYear').textContent = Utils.formatYear(p.by, t);
    document.getElementById('deathYear').textContent = Utils.formatYear(p.dy, t);

    document.getElementById('hintTxt').textContent = "";
    document.getElementById('hintBtn').style.opacity = '1';

    if (typeof updateMapMarkers === 'function') updateMapMarkers(p, t);

    const correctName = currentLang === 'en' ? (p.name_en || p.name) : p.name;
    const pool = ALL.filter(x => x.name !== p.name);
    const otherOpts = Utils.shuffle(pool).slice(0, 3).map(x => (currentLang === 'en' ? (x.name_en || x.name) : x.name));
    const opts = Utils.shuffle([correctName, ...otherOpts]);

    const grid = document.getElementById('optsGrid'); grid.innerHTML = '';
    opts.forEach(o => {
        const b = document.createElement('button'); b.className = 'opt-btn'; b.textContent = o;
        b.onclick = () => checkAns(o, correctName, b);
        grid.appendChild(b);
    });
    startTimer();
}

function startTimer() {
    clearInterval(timerInterval);
    timeLeft = currentLevel === 'easy' ? 30 : (currentLevel === 'med' ? 15 : 8);
    const timerEl = document.getElementById('timer');
    timerEl.textContent = timeLeft;
    timerInterval = setInterval(() => {
        timeLeft--;
        timerEl.textContent = timeLeft;
        if (timeLeft <= 5) {
            timerEl.classList.add('animate-pulse');
            if (timeLeft > 0) Music.sfx(400);
        }
        if (timeLeft <= 0) {
            timerEl.classList.remove('animate-pulse');
            checkAns(null, (currentLang === 'en' ? (curQ[idx].name_en || curQ[idx].name) : curQ[idx].name), null);
        }
    }, 1000);
}

function checkAns(sel, cor, btn) {
    clearInterval(timerInterval); locked = true;
    document.getElementById('timer').classList.remove('animate-pulse');

    document.querySelectorAll('.opt-btn').forEach(b => {
        b.disabled = true;
        if(b.textContent === cor) {
            b.classList.add('correct');
        } else if(btn && b === btn) {
            b.classList.add('wrong');
            Animations.shake('game-ui');
        }
    });

    if (sel === cor) {
        const p = curQ[idx];
        AchievementEvents.emit('answer_correct', { country: p.country });
        let pts = currentLevel === 'easy' ? 10 : (currentLevel === 'med' ? 15 : 25);
        if (hinted) pts = Math.floor(pts / 2);
        score += pts;
        Animations.scoreRoll(score);
        Music.sfx(800);
        Utils.vibrate(50);
        if (btn) Animations.successGlow(btn);
    } else {
        AchievementEvents.emit('answer_wrong');
        Music.sfx(200);
        Utils.vibrate(200);
    }

    setTimeout(showInfo, 1000);
}

function showInfo() {
    const p = curQ[idx];
    const t = I18N[currentLang];
    document.getElementById('infoName').textContent = currentLang === 'en' ? (p.name_en || p.name) : p.name;
    document.getElementById('infoYears').textContent = `${Utils.formatYear(p.by, t)} - ${Utils.formatYear(p.dy, t)}`;

    // Dynamic metadata
    document.getElementById('infoCountry').textContent = currentLang === 'en' ? (p.country_en || p.country || '—') : (p.country || '—');
    document.getElementById('infoEra').textContent = currentLang === 'en' ? (p.era_en || p.era || '—') : (p.era || '—');

    document.getElementById('infoBio').textContent = currentLang === 'en' ? (p.bio_en || p.bio) : p.bio;

    Animations.fadeIn('info-card', 'block');
    document.getElementById('info-card').classList.add('show');
}

function closeInfo() {
    Utils.vibrate(20);
    Music.sfx(600);
    document.getElementById('info-card').classList.remove('show');
    setTimeout(() => {
        document.getElementById('info-card').style.display = 'none';
        idx++; showQ();
    }, 500);
}

function grantHint() {
    if (hinted || locked) return;
    hinted = true;
    Utils.vibrate(20);
    Music.sfx(500);
    const p = curQ[idx];
    document.getElementById('hintTxt').textContent = currentLang === 'en' ? (p.hint_en || p.hint) : p.hint;
    document.getElementById('hintBtn').style.opacity = '0.3';
}

function onRewardedHintGranted() {
    grantHint();
    document.getElementById('hintBtn').disabled = true;
}

function onRewardedHintUnavailable() {
    if (hinted || locked) return;
    const btn = document.getElementById('hintBtn');
    btn.disabled = false;
    btn.style.opacity = '1';
}

function doHint() {
    if (hinted || locked) return;
    const btn = document.getElementById('hintBtn');
    btn.disabled = true;
    btn.style.opacity = '0.6';
    if (window.Android && Android.showRewardedHint) {
        Android.showRewardedHint();
    } else {
        grantHint();
    }
}

function endGame() {
    Music.win();
    if (window.Android && Android.showBanner) Android.showBanner();
    if (window.Android && Android.showInterstitial) Android.showInterstitial();
    AchievementEvents.emit('game_completed', { score: score });
    const isNewHigh = Storage.updateHighScore(score);
    document.getElementById('hud-bar').style.display = 'none';
    document.getElementById('game-ui').style.display = 'none';

    Animations.fadeIn('endScreen');
    document.getElementById('finalScore').textContent = score;

    if (isNewHigh) {
        document.getElementById('newBest').classList.remove('hidden');
        confetti({ particleCount: 200, spread: 80, origin: { y: 0.6 } });
    }

    const list = document.getElementById('reviewList'); list.innerHTML = '';
    curQ.forEach(p => {
        const d = document.createElement('div');
        const pName = currentLang === 'en' ? (p.name_en || p.name) : p.name;
        d.className = "p-3 bg-white/5 rounded-xl border border-white/5 text-sm font-bold flex items-center justify-between";
        d.innerHTML = `<span>${pName}</span> <i class="fa-brands fa-wikipedia-w text-blue-400"></i>`;
        d.onclick = () => window.open(`https://${currentLang}.wikipedia.org/wiki/${pName}`, '_blank');
        list.appendChild(d);
    });
}
