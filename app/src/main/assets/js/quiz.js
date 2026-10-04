const ALL = ALL_DATA;



// Strict single-language rendering for person content.
// A localized bundle must never fall back to an English field, because that
// creates mixed-language screens. Exact English copies are treated as missing
// translations for every non-English locale. Arabic metadata containing Latin
// text is also rejected rather than displayed mixed with Arabic.
const PERSON_ID_ALIASES = {
    'Napoleon Bonaparte': 'Napoleon',
    'Martin Luther King Jr.': 'Martin Luther King',
    'Omar Mukhtar': 'Omar al-Mukhtar'
};

function personBundleKey(person) {
    if (!person) return '';
    const key = person.name_en || person.name || '';
    const people = window.PERSON_I18N?.people;
    if (people?.[key]) return key;
    return PERSON_ID_ALIASES[key] || key;
}

function personLanguageBundle(person, lang = currentLang) {
    const key = personBundleKey(person);
    return window.PERSON_I18N?.people?.[key]?.languages?.[lang];
}

function englishPersonField(person, field) {
    if (!person) return undefined;
    return personLanguageBundle(person, 'en')?.[field];
}

function localizedAnswerName(person) {
    if (!person) return '';
    const localized = personLanguageBundle(person, currentLang)?.name;
    if (localized) return String(localized).trim();

    if (currentLang === 'ar') return String(person.name_ar || person.name || '').trim();
    if (currentLang === 'en') return String(person.name_en || person.name || '').trim();

    // Never inject an Arabic or English name into another language.
    return '';
}

function sanitizeLocalizedValue(value, englishValue, field) {
    if (value === undefined || value === null || value === '') return '';
    if (field === 'name') return String(value);

    if (currentLang !== 'en' && typeof value === 'string' && typeof englishValue === 'string') {
        if (value.trim() === englishValue.trim()) return '';
    }

    const text = String(value).trim();
    if (currentLang === 'ar') {
        // Metadata fields must be Arabic-only. This prevents values such as
        // "Habsburg Netherlands", "USA", or "New York City" appearing in
        // an otherwise Arabic information card.
        const metadataFields = new Set([
            'birth_city', 'birth_country', 'death_city', 'death_country', 'country', 'role', 'era'
        ]);
        if (metadataFields.has(field) && /[A-Za-z]/.test(text)) return '';
    }

    return value;
}

function localizedPersonField(person, field) {
    if (!person) return '';

    const bundle = window.PERSON_I18N?.people?.[personBundleKey(person)];
    const translated = bundle?.languages?.[currentLang]?.[field];
    const englishValue = englishPersonField(person, field);

    if (translated !== undefined && translated !== null && translated !== '') {
        if (Array.isArray(translated)) {
            const enList = Array.isArray(englishValue) ? englishValue : [];
            return translated.map((item, index) => sanitizeLocalizedValue(item, enList[index], field)).filter(Boolean);
        }
        return sanitizeLocalizedValue(translated, englishValue, field);
    }

    const native = person[`${field}_${currentLang}`];
    if (native !== undefined && native !== null && native !== '') {
        if (Array.isArray(native)) {
            const enList = Array.isArray(englishValue) ? englishValue : [];
            return native.map((item, index) => sanitizeLocalizedValue(item, enList[index], field)).filter(Boolean);
        }
        return sanitizeLocalizedValue(native, englishValue, field);
    }

    if (currentLang === 'ar') {
        return sanitizeLocalizedValue(person[field] ?? '', englishValue, field);
    }
    if (currentLang === 'en') return person[`${field}_en`] ?? '';
    return '';
}

function arabicSafePersonField(person, field) {
    return currentLang === 'ar' ? localizedPersonField(person, field) : localizedPersonField(person, field);
}

function localizedPersonList(person, field) {
    const value = localizedPersonField(person, field);
    return Array.isArray(value) ? value.filter(Boolean) : [];
}

function hasCompletePersonLanguage(person, lang = currentLang) {
    if (!person) return false;
    if (lang === 'ar') return Boolean(person.name_ar || person.name);
    if (lang === 'en') return Boolean(person.name_en || person.name);
    const bundle = window.PERSON_I18N?.people?.[personBundleKey(person)]?.languages?.[lang];
    return Boolean(bundle?.name && bundle?.bio);
}

let curQ = [], idx = 0, score = 0, currentLevel = 'easy', TOTAL_Q = 10, currentMode = 'all';
let timerInterval, timeLeft, hinted = false, locked = false, learningPhase = true, reviewMode = false;

function setMode(m, btn) {
    try {
        Utils.vibrate(20);
        Music.sfx(600);
        currentMode = m;

        // Update UI highlighting
        const buttons = document.getElementsByClassName('mode-btn');
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }

        const targetBtn = btn || document.getElementById('btnMode' + m.charAt(0).toUpperCase() + m.slice(1));
        if (targetBtn) {
            targetBtn.classList.add('active');
            targetBtn.style.transform = 'scale(0.95)';
            setTimeout(() => { targetBtn.style.transform = ''; }, 100);
        }

        if (typeof updateTotalCount === 'function') updateTotalCount();
        console.log("Mode changed to:", m);
    } catch (e) {
        console.error("Error in setMode:", e);
    }
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
        cancelPendingInterstitial();
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
    cancelPendingInterstitial();
    if (window.Android && Android.showBanner) Android.showBanner();
    Music.sfx(600);
    document.getElementById('endScreen').style.display = 'none';
    Animations.fadeIn('startScreen');
    if (map) map.setView([20, 10], 2);
}

function startGame(lv, overlayToFade = 'startScreen') {
    cancelPendingInterstitial();
    console.log("Starting game level:", lv);

    // Reveal the gameplay shell first. Initialization below must never leave
    // the user with a blank page if a non-critical WebView/Leaflet operation fails.
    const hud = document.getElementById('hud-bar');
    const gui = document.getElementById('game-ui');
    if (hud) hud.style.display = 'flex';
    if (gui) gui.style.display = 'flex';

    if (typeof Layout !== 'undefined') Layout.update();

    Animations.fadeOut(overlayToFade);
    if (window.Android && Android.hideBanner) {
        try { Android.hideBanner(); } catch (e) { console.warn('hideBanner failed:', e); }
    }

    try {
        try {
            if (typeof AchievementEvents !== 'undefined') {
                AchievementEvents.emit('game_started', { level: lv });
            }
        } catch (e) { console.warn('Achievement event failed:', e); }

        try {
            Utils.vibrate(40);
            Music.sfx(800);
            Music.unlock();
        } catch (e) {
            console.warn('Optional feedback failed:', e);
        }

        // Leaflet is visual enhancement; a map initialization problem must not
        // prevent the quiz UI from being displayed.
        try {
            if (typeof initMap === 'function') initMap();
        } catch (e) {
            console.error('Map initialization failed:', e);
        }

        currentLevel = lv;
        idx = 0;
        score = 0;
        reviewMode = false;

        const qSelect = document.getElementById('qCountSelect');
        TOTAL_Q = qSelect ? (parseInt(qSelect.value, 10) || 10) : 10;

        console.log("Preparing game for mode:", currentMode, "Level:", lv);

        const dataPool = (typeof ALL_DATA !== 'undefined') ? ALL_DATA : (typeof ALL !== 'undefined' ? ALL : []);
        if (!dataPool || dataPool.length === 0) {
            throw new Error("Critical: Data pool is empty!");
        }

        let pool = currentMode === 'all' ? dataPool : dataPool.filter(x => x.mode === currentMode);
        if (!pool || pool.length === 0) {
            console.warn("Pool is empty for mode:", currentMode, "- falling back to all.");
            pool = dataPool;
        }

        curQ = Utils.shuffle(pool).slice(0, Math.min(TOTAL_Q, pool.length));
        TOTAL_Q = curQ.length;
        console.log("Quiz initialized with", TOTAL_Q, "questions");

        if (TOTAL_Q === 0) throw new Error("No questions found in pool");

        // Give WebView/Leaflet one layout pass after the overlay disappears.
        setTimeout(() => {
            try {
                if (typeof map !== 'undefined' && map) {
                    map.invalidateSize();
                    map.setView([20, 10], 2);
                }
            } catch (e) {
                console.warn('Map resize failed:', e);
            }
            showQ();
        }, 120);
    } catch (e) {
        console.error("Critical error starting game:", e);
        if (typeof showErrorModal === 'function') {
            showErrorModal();
        } else {
            Animations.fadeIn('startScreen');
        }
    }
}

function showQ() {
    if (idx >= TOTAL_Q) { endGame(); return; }
    console.log("Showing question index:", idx);

    const gui = document.getElementById('game-ui');
    if (gui) gui.scrollTop = 0;

    const infoCard = document.getElementById('info-card');
    if (infoCard) {
        infoCard.classList.remove('show');
        infoCard.style.display = 'none';
    }
    const infoFooter = document.getElementById('info-footer');
    if (infoFooter) {
        infoFooter.style.setProperty('display', 'none', 'important');
    }

    if (typeof Layout !== 'undefined') Layout.update();

    const p = curQ[idx];
    if (!p) {
        console.error("No question data found for index:", idx);
        idx++; showQ(); return;
    }

    locked = false; hinted = false; learningPhase = true;
    const t = I18N[currentLang];

    const hTxt = document.getElementById('hintTxt');
    if (hTxt) { hTxt.textContent = ""; hTxt.style.opacity = '0'; }
    const hBtn = document.getElementById('hintBtn');
    if (hBtn) { hBtn.disabled = true; hBtn.style.opacity = '0.45'; hBtn.textContent = t.hint; }

    const qEl = document.getElementById('qCountTxt');
    if (qEl) qEl.textContent = `${idx + 1} / ${TOTAL_Q}`;

    const bYear = document.getElementById('birthYear');
    if (bYear) bYear.textContent = Utils.formatYear(p.by, t);
    const dYear = document.getElementById('deathYear');
    if (dYear) dYear.textContent = Utils.formatYear(p.dy, t);

    if (typeof updateMapMarkers === 'function') {
        try { updateMapMarkers(p, t); } catch (e) { console.error("Map Update Error:", e); }
    }

    renderLearningBrief(p, t);

    const grid = document.getElementById('optsGrid');
    if (grid) grid.style.display = 'none';
    const prompt = document.getElementById('questionPrompt');
    if (prompt) {
        prompt.style.display = 'none';
        prompt.textContent = (I18N[currentLang] || I18N.en).question_prompt;
    }
    const ready = document.getElementById('readyBtn');
    if (ready) { ready.style.display = 'block'; ready.textContent = (I18N[currentLang] || I18N.en).ready; }

    const timerEl = document.getElementById('timer');
    if (timerEl) timerEl.textContent = currentLevel === 'easy' ? 30 : (currentLevel === 'med' ? 15 : 8);
}

function buildRecallPrompt(p) {
    // Automatic hints are intentionally disabled. This function remains as a
    // compatibility helper and returns only the generic question prompt.
    const t = I18N[currentLang] || I18N.en;
    return t.question_prompt;
}

function normalizeIdentityKey(value) {
    return String(value || '')
        .normalize('NFKC')
        .replace(/[\u064B-\u065F\u0670]/g, '')
        .replace(/[‐‑‒–—−]/g, '-')
        .replace(/\s+/g, ' ')
        .trim()
        .toLocaleLowerCase();
}

function getPersonIdentityNames(person) {
    if (!person) return [];
    const names = new Set();
    [
        person.name,
        person.name_en,
        person.name_ar,
        localizedAnswerName(person)
    ].forEach(value => {
        if (value) names.add(String(value).trim());
    });

    const bundles = window.PERSON_I18N?.people?.[personBundleKey(person)]?.languages || {};
    Object.values(bundles).forEach(bundle => {
        if (bundle?.name) names.add(String(bundle.name).trim());
    });

    return [...names].filter(Boolean);
}

function getIdentityAwareDistractors(target, pool) {
    if (!target) return [];
    const targetBirth = Number(target.by);
    const targetDeath = Number(target.dy);
    const targetCategory = String(target.category || '').trim().toLowerCase();
    const targetMode = String(target.mode || '').trim().toLowerCase();

    const finiteYear = value => Number.isFinite(Number(value));
    const century = year => {
        const y = Number(year);
        if (!Number.isFinite(y)) return null;
        return y < 0 ? Math.floor(y / 100) : Math.floor((y - 1) / 100);
    };
    const eraDistance = (a, b) => {
        if (!finiteYear(a) || !finiteYear(b)) return 99;
        const ca = century(a);
        const cb = century(b);
        return Math.abs(ca - cb);
    };
    const yearDistance = (a, b) => {
        if (!finiteYear(a) || !finiteYear(b)) return Infinity;
        return Math.abs(Number(a) - Number(b));
    };
    const samePeriod = candidate => {
        if (!finiteYear(targetBirth) || !finiteYear(targetDeath) ||
            !finiteYear(candidate.by) || !finiteYear(candidate.dy)) return false;

        const tMin = Math.min(targetBirth, targetDeath);
        const tMax = Math.max(targetBirth, targetDeath);
        const cMin = Math.min(Number(candidate.by), Number(candidate.dy));
        const cMax = Math.max(Number(candidate.by), Number(candidate.dy));

        // Strong preference for overlapping lifetimes or nearby generations.
        return cMin <= tMax + 75 && cMax >= tMin - 75;
    };

    const score = candidate => {
        let value = 0;
        const candidateCategory = String(candidate.category || '').trim().toLowerCase();
        const candidateMode = String(candidate.mode || '').trim().toLowerCase();

        if (targetCategory && candidateCategory === targetCategory) value += 70;
        if (targetMode && candidateMode === targetMode) value += 8;

        const eDist = eraDistance(targetBirth, candidate.by);
        if (eDist === 0) value += 45;
        else if (eDist === 1) value += 32;
        else if (eDist === 2) value += 18;
        else if (eDist <= 4) value += 5;

        if (samePeriod(candidate)) value += 28;

        const bDist = yearDistance(targetBirth, candidate.by);
        const dDist = yearDistance(targetDeath, candidate.dy);
        if (bDist <= 25) value += 18;
        else if (bDist <= 50) value += 10;
        if (dDist <= 25) value += 12;
        else if (dDist <= 50) value += 6;

        // Avoid obviously unrelated eras even when the category happens to match.
        if (finiteYear(targetBirth) && finiteYear(candidate.by) && eraDistance(targetBirth, candidate.by) > 8) {
            value -= 80;
        }

        // Geographic proximity is a secondary signal only.
        if (Array.isArray(target.bc) && Array.isArray(candidate.bc) &&
            target.bc.length === 2 && candidate.bc.length === 2) {
            const dLat = Number(target.bc[0]) - Number(candidate.bc[0]);
            const dLon = Number(target.bc[1]) - Number(candidate.bc[1]);
            const roughKm = Math.sqrt(dLat * dLat + dLon * dLon) * 111;
            if (roughKm <= 500) value += 10;
            else if (roughKm <= 1500) value += 4;
        }

        return value;
    };

    return pool
        .filter(candidate => candidate && candidate.name !== target.name)
        .map(candidate => ({ candidate, score: score(candidate) }))
        .sort((a, b) => b.score - a.score || String(a.candidate.name).localeCompare(String(b.candidate.name)))
        .map(item => item.candidate);
}

function beginRecallChallenge() {
    if (!learningPhase || locked) return;
    learningPhase = false;
    const p = curQ[idx];
    if (!p) return;

    const correctName = localizedAnswerName(p);
    const allCandidates = ALL.filter(x => x && x.name !== p.name);
    const sameModeCandidates = allCandidates.filter(candidate =>
        String(candidate.mode || '').trim().toLowerCase() === String(p.mode || '').trim().toLowerCase()
    );

    const targetBirthYear = Number(p.by);
    const targetCentury = Number.isFinite(targetBirthYear)
        ? Math.floor(targetBirthYear < 0 ? targetBirthYear / 100 : (targetBirthYear - 1) / 100)
        : null;

    const isChronologicallyPlausible = candidate => {
        if (targetCentury === null || !Number.isFinite(Number(candidate.by))) return true;
        const candidateYear = Number(candidate.by);
        const candidateCentury = Math.floor(candidateYear < 0 ? candidateYear / 100 : (candidateYear - 1) / 100);
        return Math.abs(targetCentury - candidateCentury) <= 8;
    };

    const pickLocalized = candidates => {
        const ranked = getIdentityAwareDistractors(p, candidates);
        const result = [];
        const usedNames = new Set([normalizeIdentityKey(correctName)]);

        for (const candidate of ranked) {
            const answerName = localizedAnswerName(candidate);
            const key = normalizeIdentityKey(answerName);
            if (!answerName || !key || usedNames.has(key)) continue;
            if (!isChronologicallyPlausible(candidate)) continue;
            usedNames.add(key);
            result.push(answerName);
            if (result.length === 3) break;
        }
        return result;
    };

    // Stage 1: same quiz mode AND historically compatible period.
    let otherOpts = pickLocalized(sameModeCandidates);

    // Stage 2: if the mode metadata is too coarse (e.g. "arab" contains
    // mostly modern figures), prefer globally similar historical figures.
    if (otherOpts.length < 3) {
        otherOpts = pickLocalized(allCandidates);
    }

    // Stage 3: very old figures such as Ramesses II may not have three
    // candidates within the strict century window. Keep the same broad mode
    // rather than introducing obviously unrelated modern people.
    if (otherOpts.length < 3) {
        const rankedMode = getIdentityAwareDistractors(p, sameModeCandidates);
        const usedNames = new Set([normalizeIdentityKey(correctName), ...otherOpts.map(normalizeIdentityKey)]);
        for (const candidate of rankedMode) {
            const answerName = localizedAnswerName(candidate);
            const key = normalizeIdentityKey(answerName);
            if (!answerName || !key || usedNames.has(key)) continue;
            usedNames.add(key);
            otherOpts.push(answerName);
            if (otherOpts.length === 3) break;
        }
    }

    if (!correctName || otherOpts.length < 3) {
        console.warn('Insufficient localized distractors for', currentLang, p.name_en);
        learningPhase = true;
        return;
    }

    const opts = Utils.shuffle([correctName, ...otherOpts]);

    const ready = document.getElementById('readyBtn');
    if (ready) ready.style.display = 'none';
    // The information card is the only content shown before the player
    // starts answering. Do not inject the person's hint/bio into the
    // question prompt automatically. Hints are intentionally opt-in via
    // the light-bulb button (doHint).
    const prompt = document.getElementById('questionPrompt');
    if (prompt) {
        prompt.style.display = 'block';
        prompt.textContent = (I18N[currentLang] || I18N.en).question_prompt;
    }

    const hintTxt = document.getElementById('hintTxt');
    if (hintTxt) {
        hintTxt.textContent = '';
        hintTxt.style.opacity = '0';
        hintTxt.style.display = 'none';
    }
    const grid = document.getElementById('optsGrid');
    if (grid) {
        grid.innerHTML = '';
        grid.style.display = 'grid';
        opts.forEach(o => {
            const b = document.createElement('button');
            b.className = 'opt-btn';
            b.textContent = o;
            b.onclick = () => checkAns(o, correctName, b);
            grid.appendChild(b);
        });
    }
    const hBtn = document.getElementById('hintBtn');
    if (hBtn) {
        hBtn.disabled = false;
        hBtn.style.opacity = '1';
        hBtn.style.display = 'inline-flex';
    }
    startTimer();
}

function cardIdentityVariants(person) {
    if (!person) return [];

    const values = new Set(getPersonIdentityNames(person));
    const key = personBundleKey(person);
    const extras = {
        'Abu Nuwas': ['الحسن بن هانئ', 'الحسن بن هاني', 'Abū Nuwās'],
        'Al-Mutanabbi': ['أبو الطيب المتنبي', 'أبو الطيب', 'المتنبّي'],
        'Avicenna': ['أبو علي ابن سينا', 'Ibn Sina', 'Ibn-i Sina'],
        'Al-Khwarizmi': ['محمد بن موسى الخوارزمي', 'Muhammad ibn Musa al-Khwarizmi'],
        'Saladin': ['صلاح الدين', 'صلاح الدين يوسف بن أيوب', 'يوسف بن أيوب', 'Salah ad-Din', 'Saladino'],
        'Khalid ibn al-Walid': ['خالد بن الوليد', 'سيف الله المسلول', 'Sword of God'],
        'Ibn al-Haytham': ['الحسن بن الهيثم', 'Alhazen'],
        'Jabir ibn Hayyan': ['جابر بن حيان', 'Abu Musa Jabir ibn Hayyan'],
        'Ibn Khaldun': ['عبد الرحمن ابن خلدون', 'عبدالرحمن ابن خلدون'],
        'Al-Farabi': ['أبو نصر الفارابي'],
        'Al-Biruni': ['أبو الريحان البيروني'],
        'Ibn al-Nafis': ['علاء الدين ابن النفيس'],
        'Al-Kindi': ['أبو يوسف يعقوب بن إسحاق الكندي'],
        'Ibn Battuta': ['محمد بن عبد الله ابن بطوطة'],
        'Al-Masudi': ['علي بن الحسين المسعودي'],
        'Al-Tabari': ['محمد بن جرير الطبري'],
        'Ibn Hazm': ['علي بن أحمد ابن حزم'],
        'Ibn Arabi': ['محيي الدين ابن عربي'],
        'Abd al-Malik ibn Marwan': ['عبد الملك بن مروان'],
        'Yusuf ibn Tashfin': ['يوسف بن تاشفين'],
        'Abd al-Rahman III': ['عبد الرحمن الثالث'],
        'Tariq ibn Ziyad': ['طارق بن زياد'],
        'Amr ibn al-As': ['عمرو بن العاص'],
        'Ahmad ibn Tulun': ['أحمد بن طولون'],
        'Ibn al-Baitar': ['ضياء الدين أبو محمد عبد الله بن أحمد المالقي', 'ابن البيطار', 'ابن بیطار'],
        'Muhammad Ali': ['Cassius Marcellus Clay Jr.', 'Cassius Marcellus Clay Jr', 'Cassius Clay', 'كاسيوس كلاي'],
        'Mahatma Gandhi': ['Mohandas Karamchand Gandhi', 'موهانداس كرمشاند غاندي', 'مهاتما'],
        'Marie Curie': ['Maria Salomea Skłodowska Curie', 'Maria Skłodowska Curie'],
        'Pablo Neruda': ['Ricardo Eliécer Neftalí Reyes Basoalto'],
        'Napoleon': ['Napoleon Bonaparte', 'Napoleone di Buonaparte', 'Napoleon I'],
        'Galileo Galilei': ["Galileo di Vincenzo Bonaiuti de' Galilei", 'Galileo'],
        'Qutuz': ['Sayf ad-Din Qutuz', 'al-Malik al-Muẓaffar Sayf ad-Dīn Quṭuz', 'Kutuz', 'Kotuz'],
        'T. E. Lawrence': ['Thomas Edward Lawrence', 'Lawrence of Arabia', 'لورنس العرب', 'لورنس عربستان'],
        'Genghis Khan': ['Temüjin', 'Chinggis Khan'],
        'Alexander the Great': ['Alexander III of Macedon', 'Alexander III. von Makedonien', 'الإسكندر الثالث'],
        'Buddha': ['Siddhartha Gautama'],
        'Marcus Aurelius': ['Marcus Annius Catilius Severus', 'Marcus Catilius Severus Annius Verus'],
        'Mother Teresa': ['Agnes Gonxha Bojaxhiu'],
        'Martin Luther King': ['Michael King Jr'],
        'Martin Luther King Jr.': ['Michael King Jr'],
        'Rosa Parks': ['Rosa Louise McCauley'],
        'Augustus': ['Gaius Octavius'],
        'Catherine the Great': ['Princess Sophia Augusta Frederica'],
        'Sigmund Freud': ['Sigismund Schlomo Freud'],
        'Freddie Mercury': ['Farrokh Bulsara'],
        'George S. Patton': ['Old Blood and Guts'],
        'Louis Armstrong': ['Satchmo', 'Satchelmouth', 'Pops', 'ساتشيمو', 'بوبس'],
        'Florence Nightingale': ['The Lady with the Lamp', 'La Dame à la lampe', 'La dama de la lámpara', 'سيدة المصباح'],
        'Henri Rousseau': ['Le Douanier', '海关关员'],
        'Erwin Rommel': ['ثعلب الصحراء', 'Desert Fox', 'Löwe der Wüste'],
        'Michael Jackson': ['King of Pop', 'ملك البوب', '流行音乐之王'],
        'Elvis Presley': ['King of Rock and Roll', 'ملك الروك أند رول', '摇滚乐之王', '猫王'],
        'Elizabeth I': ['Virgin Queen', 'الملكة العذراء'],
        'Charlemagne': ['Father of Europe', '欧洲之父'],
        'Louis XIV': ['Sun King', 'پادشاه خورشید'],
        'Otto von Bismarck': ['Iron Chancellor', 'صدراعظم آهنین'],
        'Scipio Africanus': ['Africanus', 'الإفريقي'],
        'Ernest Rutherford': ['Father of Nuclear Physics', 'Vater der Kernphysik', '核物理学之父'],
        'Joseph Haydn': ['Father of the Symphony', 'Father of the String Quartet', 'Father of Sonata Form', '交响曲之父'],
        'Attila the Hun': ['Scourge of God', '上帝之鞭'],
        'Umm Kulthum': ['Kawkab al-Sharq', 'كوكب الشرق'],
        'Taha Hussein': ['عميد الأدب العربي', 'Dekan der arabischen Literatur'],
        'Ahmed Zewail': ['Ahmed Hassan Zewail', 'أحمد حسن زويل', 'father of femtochemistry', '飞秒化学之父'],
        'Ada Lovelace': ['Enchantress of Numbers', 'ساحرة الأرقام'],
        'Frederick II': ['Stupor Mundi', '世界之奇']
    };
    (extras[key] || []).forEach(value => values.add(value));

    // Build a defensive identity block from every localized name. The previous
    // implementation only removed complete names (plus a small hand-maintained
    // alias list). That allowed a surname such as "Tesla" or "Bolívar" to leak
    // into an otherwise anonymized information card. We therefore also remove
    // meaningful individual name tokens and common multi-word name tails.
    const ignoredNameTokens = new Set([
        'a', 'an', 'and', 'as', 'at', 'by', 'de', 'der', 'des', 'di', 'do', 'du',
        'el', 'la', 'le', 'los', 'of', 'the', 'van', 'von', 'ibn', 'bin', 'bint',
        'ben', 'abu', 'al', 'jr', 'sr', 'iii', 'ii', 'iv', 'i'
    ]);
    const tokenPattern = /[\p{L}\p{M}\p{N}][\p{L}\p{M}\p{N}'’.-]*/gu;
    const nameTokens = new Set();

    for (const value of [...values]) {
        const normalized = String(value || '').trim();
        if (!normalized) continue;
        const tokens = normalized.match(tokenPattern) || [];
        const meaningful = tokens
            .map(token => token.replace(/^[.]+|[.]+$/g, '').trim())
            .filter(token => token.length >= 3 && !ignoredNameTokens.has(token.toLocaleLowerCase()));

        meaningful.forEach(token => nameTokens.add(token));

        // Protect the most useful multi-word tails, e.g. "de Gaulle" and
        // "Luther King", without relying only on a full canonical name.
        for (let i = 1; i < meaningful.length; i += 1) {
            const tail = meaningful.slice(i).join(' ');
            if (tail.length >= 5) values.add(tail);
        }
    }

    // Extract aliases explicitly declared in the person's own localized text.
    // These are target aliases, not arbitrary names mentioned in the text.
    const bundle = window.PERSON_I18N?.people?.[key]?.languages || {};
    const aliasPatterns = [
        /(?:also\s+known\s+as|known\s+colloquially\s+as|known\s+as|nicknamed|born\s+as|birth\s+name)\s+(?:['“"]([^'”"]{2,100})['”"]|([^,.;:!?\n]{2,100}))/giu,
        /(?:المعروف(?:ة)?\s+ب|اشتهر(?:ت)?\s+ب|ملقب(?:اً)?\s+ب|لقب(?:ه)?\s+ب|كنيته)\s*(?:[«“"]([^»”"]{2,100})[»”"]|([^،؛.!?\n]{2,100}))/gu,
        /(?:connu\s+sous\s+le\s+nom|surnomm[ée]|conocid[oa]\s+como|apodad[oa]|bekannt\s+als|известен\s+как|dikenal\s+sebagai)\s*[:,-]?\s*(?:['“"]([^'”"]{2,100})['”"]|([^,.;:!?\n]{2,100}))/giu
    ];
    for (const language of Object.values(bundle)) {
        if (!language || typeof language !== 'object') continue;
        for (const field of ['hint', 'bio', 'achievements', 'key_facts', 'wars', 'historical_significance']) {
            const raw = language[field];
            const texts = Array.isArray(raw) ? raw : [raw];
            for (const text of texts) {
                if (typeof text !== 'string') continue;
                for (const pattern of aliasPatterns) {
                    for (const match of text.matchAll(pattern)) {
                        for (let i = 1; i < match.length; i += 1) {
                            if (match[i]) values.add(match[i].trim());
                        }
                    }
                }
            }
        }
    }

    nameTokens.forEach(token => values.add(token));

    return [...values]
        .map(value => String(value || '').trim())
        .filter(value => value.length >= 2)
        .sort((a, b) => b.length - a.length);
}

function identityRegex(value, global = false) {
    const escaped = String(value || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const flags = global ? 'giu' : 'iu';
    return new RegExp(`(?<![\\p{L}\\p{N}_])${escaped}(?![\\p{L}\\p{N}_])`, flags);
}

function containsCardIdentity(text, identities) {
    return identities.some(identity => identityRegex(identity).test(String(text || '')));
}

function splitCardSentences(text) {
    // Protect initials such as "John F. Kennedy" and "T. E. Lawrence"
    // before sentence splitting; otherwise the period after an initial is
    // mistaken for the end of a sentence and the identity can leak.
    const initialMarker = '__MAPOF_FAME_INITIAL_DOT__';
    const protectedText = String(text || '').trim()
        .replace(/\b([A-Z])\.\s+/gu, `$1${initialMarker}`)
        .replace(/([\u0600-\u06FF])\.\s+/gu, `$1${initialMarker}`)
        .replace(/\b(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s+/gu, match => match.replace(/\.\s+$/u, initialMarker));
    return protectedText
        .split(/(?<=[.!?؟。！？])\s+|\n+/u)
        .map(s => s.replaceAll(initialMarker, '. ').trim())
        .filter(Boolean);
}

function redactCardIdentity(text, person) {
    let source = String(text || '').trim();
    if (!source) return '';
    const identities = cardIdentityVariants(person);
    if (!identities.length) return source;

    const kept = [];
    for (const sentence of splitCardSentences(source)) {
        // Never expose a nickname, alternate name, birth name, or formal name.
        const identityMarker = /\b(?:better\s+known\s+as|known\s+by\s+(?:the\s+)?nickname|nicknamed|also\s+known\s+as|born\s+as|birth\s+name|full\s+name)\b|\b(?:connu\s+sous\s+le\s+nom|surnomm[ée]|conocid[oa]\s+como|apodad[oa]|bekannt\s+als|Spitzname|известен\s+как|прозвище|dikenal\s+sebagai|dijuluki)\b|(?:被称为|被稱為|愛称|呼ばれ)|(?:لقب|ملقب|الملقب|الملقبة|المعروف(?:ة)?\s+ب|اشتهر(?:ت)?\s+ب|اسمه الكامل|كنيته|لقبه)|(?:उपनाम|के नाम से|जन्म नाम)/iu;
        if (identityMarker.test(sentence)) continue;

        // Formal-name sentence: remove the entire sentence so middle/birth names cannot survive.
        if (containsCardIdentity(sentence, identities) && /\([^)]{0,160}\d{3,4}[^)]*\)/u.test(sentence)) continue;

        let cleaned = sentence;
        for (const identity of identities) {
            cleaned = cleaned.replace(identityRegex(`${identity}'s`, true), 'the');
            cleaned = cleaned.replace(identityRegex(`${identity}’s`, true), 'the');
            cleaned = cleaned.replace(identityRegex(identity, true), '');
        }
        cleaned = cleaned
            .replace(/\s+([،؛,:.!?؟。！？])/gu, '$1')
            .replace(/\s{2,}/gu, ' ')
            .replace(/(^|[\s(])[,،:;]+(?=\s|$)/gu, '$1')
            .trim();
        if (cleaned) kept.push(cleaned);
    }
    return kept.join(' ').replace(/\s{2,}/gu, ' ').trim();
}

function redactAnswer(text, p) {
    return redactCardIdentity(text, p);
}

function sanitizeCardText(text, person) {
    let out = redactCardIdentity(text, person);
    const boilerplate = [
        /^من الحقائق الموثقة عنه\s*[:：-]?\s*/u,
        /^من الحقائق الموثقة عن هذه الشخصية\s*[:：-]?\s*/u,
        /^من الحقائق الموثقة\s*[:：-]?\s*/u,
        /^Among the documented facts about this person\s*[:：-]?\s*/iu,
        /^Documented facts about this person\s*[:：-]?\s*/iu
    ];
    for (const pattern of boilerplate) out = out.replace(pattern, '');
    return out
        .replace(/\s+([،؛,:.!?؟。！？])/gu, '$1')
        .replace(/([:،؛])\s*([.。])/gu, '$2')
        .replace(/\s{2,}/gu, ' ')
        .trim();
}

function redactLearningIdentitySentences(text, person, replacement) {
    const source = String(text || '').trim();
    if (!source) return '';

    const names = getPersonIdentityNames(person)
        .map(value => String(value || '').trim())
        .filter(value => value.length >= 2)
        .sort((a, b) => b.length - a.length);

    if (!names.length) return redactAnswer(source, person);

    // Replace identities with an internal marker BEFORE sentence splitting.
    // This is important for names containing initials such as "John F. Kennedy"
    // where a naive sentence splitter would otherwise split at "F." and miss
    // the full identity.
    const marker = '__MAPOF_FAME_IDENTITY__';
    let protectedText = source;
    for (const identity of names) {
        const escaped = identity.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const exact = new RegExp(escaped, 'giu');
        protectedText = protectedText.replace(exact, marker);
    }

    // Remove any sentence that contained an identity marker. This is safer
    // than trying to guess which surname/title fragment is still identifiable.
    const sentences = protectedText.split(/(?<=[!?。！？؟])\s+|(?<=[.!])\s+(?=[\p{Lu}\p{Lt}])|\n+/u);
    const kept = sentences
        .map(sentence => sentence.trim())
        .filter(sentence => sentence && !sentence.includes(marker));

    const result = kept.join(' ').replace(/\s{2,}/g, ' ').trim();
    if (result) return redactAnswer(result, person);

    // If the source consisted entirely of identity-bearing sentences, return
    // a neutral learning placeholder rather than exposing the answer.
    return replacement;
}

function renderLearningBrief(p, t) {
    const isAr = currentLang === 'ar';
    const title = document.getElementById('learningTitle');
    const facts = document.getElementById('learningFacts');
    const bio = document.getElementById('learningBio');
    const extra = document.getElementById('learningExtra');
    const mapLabel = document.getElementById('learningMapLabel');
    const mapText = document.getElementById('learningMapPlace');
    const roleEl = document.getElementById('learningRole');
    const eraEl = document.getElementById('learningEra');
    const roleLabel = document.getElementById('learningRoleLabel');
    const eraLabel = document.getElementById('learningEraLabel');
    const overviewLabel = document.getElementById('learningOverviewLabel');

    if (title) title.textContent = t.learning_title || (isAr ? 'تعرّف على الشخصية أولاً' : 'Learn about the person');
    if (mapLabel) mapLabel.textContent = t.birth_city_lbl || (isAr ? 'مكان الميلاد' : 'Birthplace');
    if (roleLabel) roleLabel.textContent = t.category_label || (isAr ? 'الدور' : 'Role');
    if (eraLabel) eraLabel.textContent = t.era || (isAr ? 'العصر' : 'Era');
    if (overviewLabel) overviewLabel.textContent = t.overview || (isAr ? 'نبذة' : 'Overview');

    const city = localizedPersonField(p, 'birth_city');
    const country = localizedPersonField(p, 'birth_country') || localizedPersonField(p, 'country');
    const mapPlace = [city, country].filter(Boolean).join(isAr ? '، ' : ', ');
    if (mapText) mapText.textContent = mapPlace || '—';

    const role = arabicSafePersonField(p, 'role');
    const era = arabicSafePersonField(p, 'era');
    if (roleEl) roleEl.textContent = role || '—';
    if (eraEl) eraEl.textContent = era || '—';

    const localizedRole = arabicSafePersonField(p, 'role');
    const category = localizedRole || (t.cats ? (t.cats[p.category] || '') : '') || '';
    if (facts) {
        const chips = [
            mapPlace ? `📍 ${mapPlace}` : '',
            category ? `🏷️ ${category}` : '',
            p.by != null && p.dy != null ? `📅 ${Utils.formatYear(p.by, t)} – ${Utils.formatYear(p.dy, t)}` : ''
        ].filter(Boolean);
        facts.innerHTML = chips.map(x => `<span class="learning-chip">${Utils.escapeHtml ? Utils.escapeHtml(x) : x}</span>`).join('');
    }

    const rawBio = localizedPersonField(p, 'bio') || localizedPersonField(p, 'hint');
    if (bio) {
        // The learning card must never expose the answer identity. Use the same
        // strict sanitizer for the overview as for every extra fact row.
        const safeBio = sanitizeCardText(rawBio, p);
        bio.textContent = safeBio || '—';
    }

    const clean = (value) => {
        const text = String(value || '').trim();
        const placeholders = [
            'Notable historical work', 'عمل تاريخي بارز', 'Notable work', 'عمل بارز',
            'Notable event', 'حدث بارز', 'A notable historical figure in the field of',
            'شخصية تاريخية بارزة في مجال'
        ];
        if (!text || placeholders.some(x => text.includes(x))) return '';
        return text;
    };
    const list = (enKey, arKey) => {
        const field = enKey.replace('_en', '');
        return localizedPersonList(p, field).map(clean).filter(Boolean);
    };

    if (extra) {
        const achievements = list('achievements_en', 'achievements');
        const keyFacts = list('key_facts_en', 'key_facts');
        const events = list('major_wars_events_en', 'major_wars_events');
        const wars = events.length ? events : list('wars_en', 'wars');
        const significance = clean(localizedPersonField(p, 'historical_significance'));
        const rows = [];
        const addRows = (items, icon, max) => items.slice(0, max).forEach(item => {
            rows.push(`<div class="learning-extra-row"><b>${icon}</b>${Utils.escapeHtml ? Utils.escapeHtml(redactAnswer(item, p)) : redactAnswer(item, p)}</div>`);
        });
        addRows(achievements, '🏆', 2);
        addRows(keyFacts, '💡', 2);
        addRows(wars, '⚔️', 1);
        if (significance) rows.push(`<div class="learning-extra-row learning-significance"><b>⭐</b>${Utils.escapeHtml ? Utils.escapeHtml(redactAnswer(significance, p)) : redactAnswer(significance, p)}</div>`);
        extra.innerHTML = rows.join('');
    }
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
            checkAns(null, (localizedPersonField(curQ[idx], 'name')), null);
        }
    }, 1000);
}

function checkAns(sel, cor, btn) {
    if (locked) return;
    clearInterval(timerInterval);
    locked = true;

    const timer = document.getElementById('timer');
    if (timer) timer.classList.remove('animate-pulse');

    document.querySelectorAll('.opt-btn').forEach(b => {
        b.disabled = true;
        if(b.textContent === cor) {
            b.classList.add('correct');
        } else if(btn && b === btn) {
            b.classList.add('wrong');
            Animations.shake('game-ui');
        }
    });

    const answeredCorrectly = sel === cor;
    if (typeof Storage !== 'undefined' && curQ[idx]) {
        Storage.recordLearning(curQ[idx], answeredCorrectly);
        // Keep the home-screen Historical Memory counters in sync immediately
        // after every answered question.
        if (typeof refreshMemoryDashboard === 'function') refreshMemoryDashboard();
    }

    if (answeredCorrectly) {
        const p = curQ[idx];
        if (p) AchievementEvents.emit('answer_correct', { country: p.country });
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

    // Delay showing info to allow user to see correct/wrong feedback
    setTimeout(() => {
        if (locked) showInfo();
    }, 1200);
}

function showInfo() {
    const p = curQ[idx];
    const t = I18N[currentLang];
    const isAr = currentLang === 'ar';

    const infoName = document.getElementById('infoName');
    // The information card is intentionally identity-blind. The answer name,
    // surname, nickname, birth/formal name, and alternate names must never
    // appear in the card before the player has answered. The answer choices
    // remain the only place where candidate names are shown.
    if (infoName) infoName.textContent = (t && t.this_person) || (isAr ? 'هذه الشخصية' : 'This person');

    const infoYears = document.getElementById('infoYears');
    if (infoYears) infoYears.textContent = `${Utils.formatDisplayYear(p.birth_date, p.by, t)} - ${Utils.formatDisplayYear(p.death_date, p.dy, t)}`;

    // Metadata
    const infoCountry = document.getElementById('infoCountry');
    if (infoCountry) infoCountry.textContent = localizedPersonField(p, 'country') || '—';

    const infoEra = document.getElementById('infoEra');
    if (infoEra) infoEra.textContent = localizedPersonField(p, 'era') || '—';

    // Category
    const infoCategory = document.getElementById('infoCategory');
    if (infoCategory) {
        const catRaw = localizedPersonField(p, 'role') || (t.cats ? (t.cats[p.category] || '') : '') || '—';
        infoCategory.textContent = catRaw;
    }

    // Age
    const infoAge = document.getElementById('infoAge');
    if (infoAge) {
        let age = p.dy - p.by;
        if (p.by < 0 && p.dy > 0) age -= 1;
        infoAge.textContent = age > 0 ? age : '—';
    }

    const infoBirthPlace = document.getElementById('infoBirthPlace');
    // Strict separation for birth place in Info Card
    const city = localizedPersonField(p, 'birth_city');
    const country = localizedPersonField(p, 'birth_country') || localizedPersonField(p, 'country');
    const birthPlace = [city, country].filter(Boolean).join(window.RTL_LANGS && window.RTL_LANGS.has(currentLang) ? '، ' : ', ');

    if (infoBirthPlace) infoBirthPlace.textContent = birthPlace || '—';

    const achievements = localizedPersonList(p, 'achievements');
    const wars = localizedPersonList(p, 'wars');

    const IGNORE = ["Notable historical work", "عمل تاريخي بارز", "Notable work", "عمل بارز", "Notable event", "حدث بارز"];

    // Every free-text field rendered in the information card passes through
    // the same identity redaction used by the learning card. Do not rely on
    // the source data being clean: the runtime is the final safety boundary.
    const sanitizeInfoList = (list) => {
        if (!Array.isArray(list)) return [];
        return list
            .filter(item => item && !IGNORE.some(phrase => String(item).includes(phrase)))
            .map(item => sanitizeCardText(item, p))
            .filter(Boolean);
    };

    const cleanAchievements = sanitizeInfoList(achievements);
    const cleanWars = sanitizeInfoList(wars);

    const achievementsRow = document.getElementById('achievementsRow');
    const warsRow = document.getElementById('warsRow');
    const infoAchievements = document.getElementById('infoAchievements');
    const infoWars = document.getElementById('infoWars');

    if (achievementsRow) achievementsRow.style.display = cleanAchievements ? 'flex' : 'none';
    if (warsRow) warsRow.style.display = cleanWars ? 'flex' : 'none';
    if (infoAchievements) infoAchievements.textContent = cleanAchievements.length ? cleanAchievements.join(' • ') : '—';
    if (infoWars) infoWars.textContent = cleanWars.length ? cleanWars.join(' • ') : '—';

    const infoBio = document.getElementById('infoBio');
    if (infoBio) {
        const rawBio = localizedPersonField(p, 'bio');
        const safeBio = sanitizeCardText(rawBio, p);
        infoBio.textContent = safeBio || '—';
    }

    const postFacts = document.getElementById('infoKeyFacts');
    if (postFacts) {
        const factsList = sanitizeInfoList(localizedPersonList(p, 'key_facts'));
        postFacts.innerHTML = factsList.slice(0, 6).map(x => `<div class="post-fact">${Utils.escapeHtml ? Utils.escapeHtml(x) : x}</div>`).join('');
    }
    const significance = document.getElementById('infoSignificance');
    if (significance) {
        const rawSignificance = localizedPersonField(p, 'historical_significance');
        const text = sanitizeCardText(rawSignificance, p);
        significance.innerHTML = text ? `<span class="significance-title">${(I18N[currentLang] || I18N.en).why_matters}</span>${Utils.escapeHtml ? Utils.escapeHtml(text) : text}` : '';
        significance.style.display = text ? 'block' : 'none';
    }

    // Final runtime defense-in-depth: scan every free-text information-card
    // element after rendering. This protects the UI even if a future data
    // field or renderer bypasses the normal sanitizer. If an identity still
    // survives, sanitize it again and clear the element if necessary.
    const infoCardTextIds = [
        'infoBio', 'infoAchievements', 'infoWars', 'infoKeyFacts', 'infoSignificance'
    ];
    for (const id of infoCardTextIds) {
        const el = document.getElementById(id);
        if (!el) continue;
        const currentText = el.textContent || '';
        if (!containsCardIdentity(currentText, cardIdentityVariants(p))) continue;
        const cleaned = sanitizeCardText(currentText, p);
        if (containsCardIdentity(cleaned, cardIdentityVariants(p))) {
            el.textContent = '';
            if (id === 'infoSignificance') el.style.display = 'none';
        } else if (id === 'infoKeyFacts') {
            el.textContent = cleaned;
        } else {
            el.textContent = cleaned;
        }
    }

    const memoryStatus = document.getElementById('memoryStatus');
    const syncBtn = document.getElementById('syncMemoryBtn');
    if (memoryStatus && typeof Storage !== 'undefined') {
        const m = Storage.getPersonMemory(p);
        if (m) {
            const status = Storage.statusLabel ? Storage.statusLabel(m.status, currentLang) : (m.status || 'Review');
            const seenLabel = currentLang === 'ar' ? `ظهرت ${m.seen} مرة` : `${m.seen} seen`;
            const masteryLabel = currentLang === 'ar' ? `الإتقان ${m.mastery}%` : `${m.mastery}% mastery`;
            const memoryLabel = currentLang === 'ar' ? 'الذاكرة' : 'Memory';
            memoryStatus.textContent = `🧠 ${memoryLabel}: ${status} • ${seenLabel} • ${masteryLabel}`;
        } else {
            memoryStatus.textContent = '';
        }
        if (syncBtn) {
            syncBtn.disabled = !m;
            syncBtn.textContent = t.sync_memory || (isAr ? 'حفظ حالة الذاكرة' : 'Sync mastery status');
            syncBtn.dataset.synced = m && m.syncedAt ? 'true' : 'false';
        }
    }

    const btnNextTxt = document.getElementById('btnNextTxt');
    const btnNextIcon = document.getElementById('btnNextIcon');
    const isLast = idx >= TOTAL_Q - 1;

    if (btnNextTxt) {
        btnNextTxt.textContent = isLast ? t.result : t.next;
    }
    if (btnNextIcon) {
        btnNextIcon.className = isLast ? 'fa-solid fa-flag-checkered text-xl' : 'fa-solid fa-forward-step text-xl ltr:rotate-0 rtl:rotate-180';
    }

    const hud = document.getElementById('hud-bar');
    if (hud) hud.style.opacity = '0';

    const card = document.getElementById('info-card');
    const footer = document.getElementById('info-footer');
    if (card) {
        card.scrollTop = 0;
        card.style.display = 'flex';
        // Force reflow before opening the info screen.
        card.offsetHeight;
        card.classList.add('show');
        if (typeof Layout !== 'undefined') Layout.update();
        if (typeof map !== 'undefined' && map) map.invalidateSize();
        if (footer) footer.style.setProperty('display', 'flex', 'important');
    }
}


function syncCurrentMemory() {
    const p = curQ[idx];
    if (!p || typeof Storage === 'undefined' || !Storage.markMasterySynced) return;
    const memory = Storage.markMasterySynced(p);
    const btn = document.getElementById('syncMemoryBtn');
    if (btn) {
        btn.dataset.synced = 'true';
        btn.textContent = currentLang === 'en' ? 'Mastery status saved' : 'تم حفظ حالة الذاكرة';
    }
    const status = document.getElementById('memoryStatus');
    if (status && memory) status.textContent = currentLang === 'en'
        ? `🧠 Memory: ${Storage.statusLabel(memory.status, currentLang)} • ${memory.mastery}% mastery • synced`
        : `🧠 الذاكرة: ${Storage.statusLabel(memory.status, currentLang)} • الإتقان ${memory.mastery}% • تم الحفظ`;
}

function closeInfo() {
    Utils.vibrate(20);
    Music.sfx(600);
    const infoCard = document.getElementById('info-card');
    if (!infoCard) return;

    infoCard.classList.remove('show');
    if (typeof Layout !== 'undefined') Layout.update();
    if (typeof map !== 'undefined' && map) map.invalidateSize();

    // Hide the fixed footer immediately so its buttons can never sit above
    // the answer grid while the next question is being rendered.
    const footer = document.getElementById('info-footer');
    if (footer) footer.style.setProperty('display', 'none', 'important');

    const hud = document.getElementById('hud-bar');
    if (hud) hud.style.opacity = '1';

    const isLast = idx >= TOTAL_Q - 1;

    // Smoothly wait for the slide-down animation to complete
    // This prevents the "white gap" during transition
    setTimeout(() => {
        infoCard.style.display = 'none';
        idx++;
        if (isLast) endGame();
        else showQ();
    }, 600);
}

function grantHint() {
    console.log("grantHint called. hinted:", hinted, "locked:", locked);
    if (hinted || locked) return;

    if (window.hintSafetyTimeout) clearTimeout(window.hintSafetyTimeout);

    const p = curQ[idx];
    if (!p) return;

    hinted = true;
    Utils.vibrate(20);
    Music.sfx(500);

    const hintText = localizedPersonField(p, 'hint');
    const el = document.getElementById('hintTxt');
    if (el) {
        el.textContent = hintText;
        el.style.opacity = '1';
        el.style.display = 'block'; // Ensure it's not hidden
    }

    const btn = document.getElementById('hintBtn');
    if (btn) {
        btn.style.opacity = '0.3';
        btn.disabled = true;
        btn.textContent = (I18N[currentLang] || I18N.en).used;
    }
}

// Ensure these are globally accessible for Android WebView
window.onRewardedHintGranted = function() {
    console.log("Global onRewardedHintGranted called");
    grantHint();
};

window.onRewardedHintUnavailable = function() {
    console.log("Global onRewardedHintUnavailable called - Fallback to free hint");
    if (window.hintSafetyTimeout) clearTimeout(window.hintSafetyTimeout);

    // If ad is unavailable, just grant the hint for free instead of making user wait
    grantHint();
};


function doHint() {
    console.log("doHint triggered. hinted:", hinted, "locked:", locked);
    if (hinted || locked) return;

    // Show optional rewarded ad confirmation modal to comply with Families Ad Format Requirements
    const modal = document.getElementById('rewardHintModal');
    if (modal) {
        modal.style.display = 'flex';
        Animations.fadeIn('rewardHintModal');
    } else {
        proceedWithHintAd();
    }
}

function confirmWatchRewardedHint(watch) {
    Animations.fadeOut('rewardHintModal', () => {
        const modal = document.getElementById('rewardHintModal');
        if (modal) modal.style.display = 'none';
        if (watch) {
            proceedWithHintAd();
        } else {
            const btn = document.getElementById('hintBtn');
            if (btn) btn.disabled = false;
        }
    });
}

function proceedWithHintAd() {
    const btn = document.getElementById('hintBtn');
    if (btn) {
        btn.disabled = true;
        btn.style.opacity = '0.5';
        btn.textContent = "...";
    }

    const hintTxt = document.getElementById('hintTxt');
    if (hintTxt) {
        hintTxt.style.opacity = '1';
        hintTxt.style.display = 'block';
        hintTxt.textContent = (I18N[currentLang] || I18N.en).loading_hint;
    }

    if (window.Android && typeof Android.showRewardedHint === 'function') {
        try {
            window.hintSafetyTimeout = setTimeout(() => {
                if (!hinted) {
                    console.warn("Safety timeout: granting free hint.");
                    grantHint();
                }
            }, 8000); // Slightly longer for slower connections
            Android.showRewardedHint();
        } catch (e) {
            console.error("Android call failed:", e);
            grantHint();
        }
    } else {
        grantHint();
    }
}


function refreshMemoryDashboard() {
    if (typeof Storage === 'undefined') return;
    const s = Storage.getLearningSummary();
    const set = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value; };
    set('memoryLearned', s.learned);
    set('memoryReview', s.review);
    set('memoryFailed', s.failed || 0);
    set('memoryMastered', s.mastered);
    const btn = document.getElementById('reviewMemoryBtn');
    if (btn) { btn.disabled = (s.activeReview || s.review || s.failed || 0) === 0; btn.style.opacity = btn.disabled ? '0.45' : '1'; }
}

function startReviewGame() {
    const review = typeof Storage !== 'undefined' ? Storage.getReviewCharacters(ALL) : [];
    if (!review.length) return;
    reviewMode = true; idx = 0; score = 0; currentLevel = 'easy';
    const qSelect = document.getElementById('qCountSelect');
    TOTAL_Q = Math.min(parseInt(qSelect ? qSelect.value : '10', 10) || 10, review.length);
    curQ = Utils.shuffle(review).slice(0, TOTAL_Q); TOTAL_Q = curQ.length;
    Animations.fadeOut('startScreen');
    if (window.Android && Android.hideBanner) Android.hideBanner();
    document.getElementById('hud-bar').style.display = 'flex';
    document.getElementById('game-ui').style.display = 'flex';
    setTimeout(() => { if (map) { map.invalidateSize(); map.setView([20,10],2); } showQ(); }, 300);
}

function cancelPendingInterstitial() {
    if (window.pendingInterstitialTimeout) {
        clearTimeout(window.pendingInterstitialTimeout);
        window.pendingInterstitialTimeout = null;
    }
}

function restartGame() {
    Utils.vibrate(30);
    Music.sfx(600);
    cancelPendingInterstitial();
    if (window.Android && Android.hideBanner) Android.hideBanner();
    // Hide end screen
    document.getElementById('endScreen').style.display = 'none';
    // Restart with same level
    startGame(currentLevel);
}

function continueGame() {
    Utils.vibrate(30);
    Music.sfx(600);
    cancelPendingInterstitial();
    if (window.Android && Android.hideBanner) Android.hideBanner();

    // Reset flags but keep score and achievements
    idx = 0;
    locked = false;
    hinted = false;

    // Hide end screen
    document.getElementById('endScreen').style.display = 'none';

    // Reshuffle and get new questions from the current mode pool
    let pool = currentMode === 'all' ? ALL : ALL.filter(x => x.mode === currentMode);
    curQ = Utils.shuffle(pool).slice(0, Math.min(TOTAL_Q, pool.length));
    TOTAL_Q = curQ.length;

    // Show UI and first question
    document.getElementById('hud-bar').style.display = 'flex';
    document.getElementById('game-ui').style.display = 'flex';
    if (map) {
        map.invalidateSize();
        map.setView([20, 10], 2);
    }
    showQ();
}

function nextLevel() {
    cancelPendingInterstitial();
    const nextLv = currentLevel === 'easy' ? 'med' : (currentLevel === 'med' ? 'hard' : null);
    if (nextLv) {
        score = 0;
        // Direct transition from endScreen to next level
        startGame(nextLv, 'endScreen');
    }
}


function endGame() {
    console.log("Entering endGame...");
    Music.win();

    if (window.Android && Android.showBanner) Android.showBanner();

    cancelPendingInterstitial();

    // Delay interstitial to prevent transition stutter with active endScreen visibility check
    if (window.Android && Android.showInterstitial) {
        window.pendingInterstitialTimeout = setTimeout(() => {
            const endScreenEl = document.getElementById('endScreen');
            if (endScreenEl && endScreenEl.style.display !== 'none' && window.Android && Android.showInterstitial) {
                Android.showInterstitial();
            }
            window.pendingInterstitialTimeout = null;
        }, 1200);
    }

    AchievementEvents.emit('game_completed', { score: score });
    if (typeof refreshMemoryDashboard === 'function') refreshMemoryDashboard();
    const isNewHigh = Storage.updateHighScore(score);

    // Show end screen first to cover the UI
    Animations.fadeIn('endScreen');

    // Hide game elements with a longer delay to ensure endScreen is solid
    setTimeout(() => {
        const hud = document.getElementById('hud-bar');
        const gui = document.getElementById('game-ui');
        if (hud) hud.style.display = 'none';
        if (gui) gui.style.display = 'none';
    }, 500);

    const finalScoreEl = document.getElementById('finalScore');
    if (finalScoreEl) finalScoreEl.textContent = score;

    const btnNL = document.getElementById('btnNextLevel');
    if (btnNL) {
        if (currentLevel === 'easy' || currentLevel === 'med') {
            btnNL.classList.remove('hidden');
            btnNL.style.display = 'flex';
        } else {
            btnNL.classList.add('hidden');
            btnNL.style.display = 'none';
        }
    }

    if (isNewHigh) {
        const newBest = document.getElementById('newBest');
        if (newBest) newBest.classList.remove('hidden');
        // Keep the new-record message without canvas-confetti to avoid WebView flash frames.
    }

    const list = document.getElementById('reviewList');
    if (list) {
        list.innerHTML = '';
        // Only show first 10 for performance if many questions
        const reviewPool = curQ.slice(0, 15);
        reviewPool.forEach(p => {
            const d = document.createElement('div');
            const pName = localizedPersonField(p, 'name');
            d.className = "p-3 rounded-xl border review-item text-sm font-bold flex items-center justify-between cursor-pointer active:scale-95 transition-transform";
            d.innerHTML = `<span>${pName}</span> <i class="fa-brands fa-wikipedia-w"></i>`;
            d.onclick = () => {
                if (typeof openWikiExtended === 'function') openWikiExtended(p);
                else window.open(`https://${currentLang}.wikipedia.org/wiki/${encodeURIComponent(pName)}`, '_blank');
            };
            list.appendChild(d);
        });
    }
}
