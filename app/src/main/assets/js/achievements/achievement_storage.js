const AchievementStorage = (() => {
    const KEY = 'unlocked_achievements';
    const safeParse = (raw) => {
        if (!raw) return {};
        try {
            const value = JSON.parse(raw);
            return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
        } catch (error) {
            console.warn('Ignoring corrupted achievement storage:', error);
            return {};
        }
    };

    return {
        getUnlocked: () => safeParse(localStorage.getItem(KEY)),
        saveUnlock: (id) => {
            const unlocked = safeParse(localStorage.getItem(KEY));
            unlocked[id] = {
                date: new Date().toISOString().split('T')[0],
                unlocked: true
            };
            localStorage.setItem(KEY, JSON.stringify(unlocked));
        }
    };
})();
