const AchievementUI = {
    notify: (ach, rewardResult) => {
        const title = ach.title[currentLang];
        const toast = document.createElement('div');
        toast.className = 'achievement-toast';
        toast.innerHTML = `
            <div class="ach-icon"><i class="fa-solid fa-${ach.icon}"></i></div>
            <div class="ach-details">
                <div class="ach-msg">${currentLang === 'en' ? 'Achievement Unlocked!' : 'تم فتح إنجاز جديد!'}</div>
                <div class="ach-title">${title}</div>
                <div class="ach-xp">+${ach.reward} XP</div>
            </div>
        `;
        document.body.appendChild(toast);
        Music.sfx(800);
        Utils.vibrate(100);

        setTimeout(() => toast.classList.add('show'), 100);

        if (rewardResult.leveledUp) {
            setTimeout(() => AchievementUI.levelUp(rewardResult.level), 3000);
        }

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 1000);
        }, 5000);
    },

    levelUp: (level) => {
        const toast = document.createElement('div');
        toast.className = 'achievement-toast level-up';
        toast.innerHTML = `
            <div class="ach-icon"><i class="fa-solid fa-arrow-up"></i></div>
            <div class="ach-details">
                <div class="ach-msg">${currentLang === 'en' ? 'Level Up!' : 'ارتفع مستواك!'}</div>
                <div class="ach-title">${currentLang === 'en' ? 'Level' : 'المستوى'} ${level}</div>
            </div>
        `;
        document.body.appendChild(toast);
        confetti({ particleCount: 150, spread: 70, origin: { y: 0.2 } });
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 1000);
        }, 4000);
    },

    openDashboard: () => {
        const stats = Stats.get();
        const unlocked = AchievementStorage.getUnlocked();

        const overlay = document.createElement('div');
        overlay.id = 'ach-dashboard';
        overlay.className = 'overlay dashboard-view';

        let html = `
            <div class="dash-header">
                <button onclick="AchievementUI.close()" class="back-btn"><i class="fa-solid fa-arrow-right"></i></button>
                <h2 class="text-2xl font-black">${currentLang === 'en' ? 'Achievements' : 'الإنجازات'}</h2>
                <div class="lvl-badge">LV ${stats.level}</div>
            </div>
            <div class="dash-content">
        `;

        ACHIEVEMENT_DATA.forEach(ach => {
            const isUnlocked = !!unlocked[ach.id];
            let progress = 0;
            let current = 0;

            if (ach.condition === 'countriesVisited') {
                current = stats.countriesVisited.length;
            } else {
                current = stats[ach.condition];
            }

            progress = Math.min((current / ach.target) * 100, 100);

            html += `
                <div class="ach-card ${isUnlocked ? 'unlocked' : ''}">
                    <div class="ach-card-icon"><i class="fa-solid fa-${ach.icon}"></i></div>
                    <div class="ach-card-info">
                        <div class="ach-card-title">${ach.title[currentLang]}</div>
                        <div class="ach-card-desc">${ach.desc[currentLang]}</div>
                        <div class="progress-wrap">
                            <div class="progress-bar" style="width: ${progress}%"></div>
                        </div>
                        <div class="progress-meta">
                            <span>${current} / ${ach.target}</span>
                            <span>${Math.floor(progress)}%</span>
                        </div>
                    </div>
                </div>
            `;
        });

        html += `</div>`;
        overlay.innerHTML = html;
        document.body.appendChild(overlay);
        Animations.fadeIn('ach-dashboard');
    },

    close: () => {
        Animations.fadeOut('ach-dashboard');
        setTimeout(() => document.getElementById('ach-dashboard').remove(), 400);
    }
};
