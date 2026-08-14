const Storage = (() => {
    return {
        saveSettings: (settings) => {
            localStorage.setItem('game_settings', JSON.stringify(settings));
        },
        getSettings: () => {
            const defaults = { lang: 'ar', theme: 'dark', lastMode: 'all', lastDiff: 'easy' };
            const saved = localStorage.getItem('game_settings');
            return saved ? { ...defaults, ...JSON.parse(saved) } : defaults;
        },
        updateHighScore: (score) => {
            let high = localStorage.getItem('highScore') || 0;
            if (score > high) {
                localStorage.setItem('highScore', score);
                return true;
            }
            return false;
        },
        getHighScore: () => localStorage.getItem('highScore') || 0,
        unlockAchievement: (id) => {
            let unlocked = JSON.parse(localStorage.getItem('achievements') || '[]');
            if (!unlocked.includes(id)) {
                unlocked.push(id);
                localStorage.setItem('achievements', JSON.stringify(unlocked));
                return true;
            }
            return false;
        },
        getAchievements: () => JSON.parse(localStorage.getItem('achievements') || '[]')
    };
})();
