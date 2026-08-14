const AchievementStorage = (() => {
    const KEY = 'unlocked_achievements';

    return {
        getUnlocked: () => {
            return JSON.parse(localStorage.getItem(KEY) || '{}');
        },
        saveUnlock: (id) => {
            const unlocked = JSON.parse(localStorage.getItem(KEY) || '{}');
            unlocked[id] = {
                date: new Date().toISOString().split('T')[0],
                unlocked: true
            };
            localStorage.setItem(KEY, JSON.stringify(unlocked));
        }
    };
})();
