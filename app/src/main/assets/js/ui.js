let currentLang = 'en';

function toggleLanguage() {
    Utils.vibrate(30);
    Music.sfx(600);
    openLanguagePicker();
}

function openLanguagePicker() {
    const modal = document.getElementById('languagePicker');
    const list = document.getElementById('languageOptions');
    if (!modal || !list || !window.LANGUAGES) return;
    list.innerHTML = window.LANGUAGES.map(([code, nativeName]) => {
        const active = code === currentLang ? ' active' : '';
        return `<button type="button" class="language-option${active}" onclick="chooseLanguage('${code}')"><span class="language-code">${code.toUpperCase()}</span><span>${nativeName}</span>${active ? '<i class="fa-solid fa-check"></i>' : ''}</button>`;
    }).join('');
    const title = document.getElementById('languagePickerTitle');
    if (title) title.textContent = (I18N[currentLang] && I18N[currentLang].choose_language) || 'Choose language';
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
}

function closeLanguagePicker() {
    const modal = document.getElementById('languagePicker');
    if (!modal) return;
    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
}

function chooseLanguage(code) {
    if (!I18N[code]) return;
    setLanguage(code);
    Storage.saveSettings({ lang: code });
    closeLanguagePicker();
}

function setLanguage(l) {
    console.log("Setting language to:", l);
    currentLang = l;
    const body = document.body;
    const isRtl = window.RTL_LANGS ? window.RTL_LANGS.has(l) : (l === 'ar');

    // Use classList to preserve other classes like 'light-theme'
    if (isRtl) {
        body.classList.remove('ltr');
        body.classList.add('rtl');
    } else {
        body.classList.remove('rtl');
        body.classList.add('ltr');
    }

    document.documentElement.lang = l;
    document.documentElement.dir = isRtl ? 'rtl' : 'ltr';

    const toggleBtn = document.getElementById('langToggle');
    if (toggleBtn) {
        toggleBtn.style.borderColor = isRtl ? '#f0a500' : '#2ec4b6';
        toggleBtn.style.color = isRtl ? '#f0a500' : '#2ec4b6';
    }

    const t = I18N[l] || I18N.en;
    const isEn = l === 'en';
    if (typeof refreshMemoryDashboard === 'function') refreshMemoryDashboard();
    document.getElementById('mainTitle').textContent = t.title;
    document.title = t.title;

    updateTotalCount();

    document.getElementById('lblMode').textContent = t.play_mode;
    document.getElementById('btnModeAll').textContent = t.all;
    document.getElementById('btnModeArab').textContent = t.arab;
    document.getElementById('btnModeIslamic').textContent = t.islamic;
    document.getElementById('btnModeMedieval').textContent = t.medieval;
    document.getElementById('btnModeModern').textContent = t.modern;
    document.getElementById('btnModeAncient').textContent = t.ancient;
    document.getElementById('lblQCount').textContent = t.q_count;
    document.getElementById('opt5').textContent = t.q5;
    document.getElementById('opt10').textContent = t.q10;
    document.getElementById('opt20').textContent = t.q20;
    document.getElementById('opt50').textContent = t.q50;
    document.getElementById('optAll').textContent = t.q_all;
    document.getElementById('lblDiff').textContent = t.difficulty;

    // Difficulty buttons
    document.getElementById('btnDiffEasy').textContent = t.easy;
    document.getElementById('btnDiffMed').textContent = t.med;
    document.getElementById('btnDiffHard').textContent = t.hard;

    document.getElementById('lblHighScore').textContent = t.high_score;
    document.getElementById('lblBirth').textContent = t.birth;
    document.getElementById('lblDeath').textContent = t.death;
    document.getElementById('hintBtn').textContent = t.hint;
    document.getElementById('btnNextTxt').textContent = t.next;
    document.getElementById('lblFinalTitle').textContent = t.final_score;
    document.getElementById('newBest').textContent = t.new_best;
    document.getElementById('lblReview').textContent = t.review;

    const setText = (id, value) => { const el = document.getElementById(id); if (el) el.textContent = value; };
    setText('memoryDashboardTitle', t.memory_title);
    setText('memoryLearnedLabel', t.memory_learned);
    setText('memoryReviewLabel', t.memory_review);
    setText('memoryFailedLabel', t.memory_failed || (isEn ? 'Failed' : 'أخطأت بها'));
    setText('memoryMasteredLabel', t.memory_mastered);
    setText('reviewMemoryBtn', t.review_memory);
    setText('deepLearningTitle', t.deep_learning_title || (isEn ? 'Deep learning & memory sync' : 'تعلّم أعمق وتثبيت الذاكرة'));
    setText('learningMapLabel', t.birth_city_lbl || (isEn ? 'Birthplace / event' : 'مكان الولادة / الحدث'));
    setText('syncMemoryBtn', t.sync_memory || (isEn ? 'Sync mastery status' : 'حفظ حالة الذاكرة'));

    // End screen bar labels
    if (document.getElementById('lblReplayTxt')) document.getElementById('lblReplayTxt').textContent = t.replay;
    if (document.getElementById('lblContinueTxt')) document.getElementById('lblContinueTxt').textContent = t.continue_btn;
    if (document.getElementById('lblNextLevelTxt')) document.getElementById('lblNextLevelTxt').textContent = t.next_level;
    if (document.getElementById('lblHomeTxt')) document.getElementById('lblHomeTxt').textContent = t.home;

    document.getElementById('lblShare').textContent = t.share;

    // Exit Modal translations
    document.getElementById('lblExitTitle').textContent = t.exit_title;
    document.getElementById('btnExitYes').textContent = t.yes;
    document.getElementById('btnExitNo').textContent = t.no;

    // Wiki Modal translations
    const msg1 = document.getElementById('wikiMsg1');
    if (msg1) msg1.textContent = t.wiki_not_found;
    const msg2 = document.getElementById('wikiMsg2');
    if (msg2) msg2.textContent = t.wiki_ask_en;
    const btnEn = document.getElementById('btnWikiEn');
    if (btnEn) btnEn.textContent = t.view_en;
    const btnCan = document.getElementById('btnWikiCancel');
    if (btnCan) btnCan.textContent = t.cancel;

    // Detailed Info Card labels
    document.getElementById('lblCountry').textContent = t.country;
    document.getElementById('lblEra').textContent = t.era;
    document.getElementById('lblCategory').textContent = t.category_label;
    document.getElementById('lblAge').textContent = t.age_label;
    document.getElementById('btnWiki').textContent = t.wiki;

    // Privacy buttons
    document.getElementById('privacyBtn').textContent = t.privacy_policy;

    // Settings Modal translations
    setText('lblSettingsTitle', t.settings);
    setText('lblThemeToggle', t.theme_toggle_label);
    setText('lblAboutApp', t.about_app);
    setText('lblPrivacyPolicy', t.privacy_policy);
    setText('lblRateApp', t.rate_app);
    setText('lblShareApp', t.share_app);
    setText('lblTermsOfUse', t.terms_of_use);
    setText('lblResetApp', t.reset_app);
    const choicesBtn = document.getElementById('privacyChoicesBtn');
    if (choicesBtn) choicesBtn.textContent = t.privacy_choices;

    // Correct form alignment
    const startForm = document.getElementById('startForm');
    if (startForm) {
        startForm.classList.toggle('text-right', isRtl);
        startForm.classList.toggle('text-left', !isRtl);
    }
    const reviewArea = document.getElementById('reviewArea');
    if (reviewArea) {
        reviewArea.classList.toggle('text-right', isRtl);
        reviewArea.classList.toggle('text-left', !isRtl);
    }

    Layout.update();
}

/**
 * Layout Manager: Controls the dynamic distribution of space between Map and UI.
 */
const Layout = {
    config: {
        mapRatio: 0.45, // Balanced map ratio for gameplay and result view.
        minMapH: 155,
        maxMapH: 320,
        hudH: 64
    },

    update: () => {
        const h = window.innerHeight;
        const w = window.innerWidth;
        let safeTop = 0;
        let safeBottom = 0;

        // Fetch precise metrics from Android if available
        if (window.Android && Android.getDisplayMetrics) {
            try {
                const m = JSON.parse(Android.getDisplayMetrics());
                const density = m.density || 1;
                safeTop = m.safeTop / density;
                safeBottom = m.safeBottom / density;
            } catch (e) {
                console.warn("Failed to parse Android metrics:", e);
            }
        }

        const { mapRatio, minMapH, maxMapH, hudH } = Layout.config;
        const infoCardOpen = document.getElementById('info-card') && document.getElementById('info-card').classList.contains('show');
        const activeRatio = infoCardOpen ? 0.32 : mapRatio;
        const activeMaxH = infoCardOpen ? 220 : maxMapH;

        // Calculate available space for Map + Game UI / Info Card
        const available = h - safeTop - hudH;

        // Calculate Map Height
        let mapH = Math.floor(available * activeRatio);
        if (mapH < minMapH) mapH = minMapH;
        if (mapH > activeMaxH) mapH = activeMaxH;

        // Apply to Map Area
        const mapArea = document.getElementById('map-area');
        if (mapArea) {
            mapArea.style.top = (safeTop + hudH) + 'px';
            mapArea.style.height = mapH + 'px';
        }

        // Apply to Game UI
        const gui = document.getElementById('game-ui');
        if (gui) {
            const guiTop = safeTop + hudH + mapH;
            const guiH = h - guiTop;
            gui.style.top = guiTop + 'px';
            gui.style.height = guiH + 'px';
            gui.style.paddingBottom = (20 + safeBottom) + 'px';
        }

        // Apply to Info Card
        const infoCard = document.getElementById('info-card');
        if (infoCard) {
            const guiTop = safeTop + hudH + mapH;
            const guiH = h - guiTop;
            infoCard.style.top = guiTop + 'px';
            infoCard.style.height = guiH + 'px';
            infoCard.style.paddingBottom = (20 + safeBottom) + 'px';
        }

        // Apply to HUD
        const hudEl = document.getElementById('hud-bar');
        if (hudEl) {
            hudEl.style.top = safeTop + 'px';
        }

        // Update Leaflet if initialized
        if (typeof map !== 'undefined' && map) {
            map.invalidateSize();
        }

        console.log(`Layout Sync: Map=${mapH}px, UI=${h - (safeTop + hudH + mapH)}px`);
    },

    // Experimentation Helpers
    setMapSize: (preset) => {
        switch(preset) {
            case 'small':  Layout.config.mapRatio = 0.25; Layout.config.maxMapH = 200; break;
            case 'medium': Layout.config.mapRatio = 0.38; Layout.config.maxMapH = 320; break;
            case 'large':  Layout.config.mapRatio = 0.48; Layout.config.maxMapH = 420; break;
        }
        Layout.update();
    }
};

window.addEventListener('resize', () => {
    Layout.update();
});

document.addEventListener('DOMContentLoaded', () => {
    Layout.update();
    // Safety re-sync after a short delay for late-rendering ads/insets
    setTimeout(Layout.update, 500);
});

function shareScore() {
    Utils.vibrate(30);
    Music.sfx(600);
    const t = I18N[currentLang];
    const text = t.share_text.replace("{score}", score);
    Utils.share(text);
}

function shareApp() {
    Utils.vibrate(30);
    Music.sfx(600);
    const t = I18N[currentLang] || I18N.en;
    const text = `${t.title || 'Map of Fame'}\nhttps://play.google.com/store/apps/details?id=com.adamos.mapoffame`;
    Utils.share(text);
}

function updateTotalCount() {
    const data = (typeof ALL_DATA !== 'undefined') ? ALL_DATA : (typeof ALL !== 'undefined' ? ALL : []);
    if (data.length === 0) return;
    const mode = (typeof currentMode !== 'undefined') ? currentMode : 'all';
    const filtered = mode === 'all' ? data : data.filter(x => x.mode === mode);
    const count = filtered.length;
    const t = I18N[currentLang] || I18N.en;
    const cap = document.getElementById('totalCap');
    if (cap) {
        cap.textContent = `${t.subtitle} (${count})`;
    }
}

