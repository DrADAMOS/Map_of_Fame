let currentLang = 'ar';

function toggleLanguage() {
    Utils.vibrate(30);
    Music.sfx(600);
    const newLang = currentLang === 'ar' ? 'en' : 'ar';
    setLanguage(newLang);
    Storage.saveSettings({ lang: newLang });
}

function setLanguage(l) {
    console.log("Setting language to:", l);
    currentLang = l;
    const body = document.body;
    const isEn = l === 'en';
    body.className = isEn ? 'ltr' : 'rtl';
    document.documentElement.lang = l;
    document.documentElement.dir = isEn ? 'ltr' : 'rtl';

    const toggleBtn = document.getElementById('langToggle');
    if (toggleBtn) {
        toggleBtn.textContent = isEn ? 'EN' : 'AR';
        toggleBtn.style.borderColor = isEn ? '#2ec4b6' : '#f0a500';
        toggleBtn.style.color = isEn ? '#2ec4b6' : '#f0a500';
    }

    const t = I18N[l];
    document.getElementById('mainTitle').textContent = t.title;
    document.title = t.title;

    const totalCount = (typeof ALL !== 'undefined') ? ALL.length : 0;
    document.getElementById('totalCap').textContent = isEn ? `Explore History (${totalCount} characters)` : `استكشف رحلة التاريخ (${totalCount} شخصية)`;

    document.getElementById('lblMode').textContent = t.play_mode;
    document.getElementById('btnModeAll').textContent = t.all;
    document.getElementById('btnModeArab').textContent = t.arab;
    document.getElementById('btnModeIslamic').textContent = t.islamic;
    document.getElementById('btnModeModern').textContent = t.modern;
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
    document.getElementById('btnNext').textContent = t.next;
    document.getElementById('lblFinalTitle').textContent = t.final_score;
    document.getElementById('newBest').textContent = t.new_best;
    document.getElementById('lblReview').textContent = t.review;
    document.getElementById('btnReplay').textContent = t.replay;
    document.getElementById('lblShare').textContent = t.share;

    // Exit Modal translations
    document.getElementById('lblExitTitle').textContent = t.exit_title;
    document.getElementById('btnExitYes').textContent = t.yes;
    document.getElementById('btnExitNo').textContent = t.no;

    // Detailed Info Card labels
    document.getElementById('lblCountry').textContent = t.country;
    document.getElementById('lblEra').textContent = t.era;
    document.getElementById('btnWiki').textContent = t.wiki;

    // Correct form alignment
    const startForm = document.getElementById('startForm');
    if (startForm) {
        startForm.classList.toggle('text-right', !isEn);
        startForm.classList.toggle('text-left', isEn);
    }
    const reviewArea = document.getElementById('reviewArea');
    if (reviewArea) {
        reviewArea.classList.toggle('text-right', !isEn);
        reviewArea.classList.toggle('text-left', isEn);
    }
}

function shareScore() {
    Utils.vibrate(30);
    Music.sfx(600);
    const t = I18N[currentLang];
    const text = t.share_text.replace("{score}", score);
    Utils.share(text);
}
