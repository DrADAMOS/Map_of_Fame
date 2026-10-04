const Stats = (() => {
    const KEY = 'game_stats';
    let data = {
        correctAnswers: 0,
        wrongAnswers: 0,
        countriesVisited: [],
        longestStreak: 0,
        currentStreak: 0,
        gamesPlayed: 0,
        xp: 0,
        level: 1
    };

    const load = () => {
        const saved = localStorage.getItem(KEY);
        if (!saved) return;
        try {
            const parsed = JSON.parse(saved);
            if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
                data = { ...data, ...parsed };
                if (!Array.isArray(data.countriesVisited)) data.countriesVisited = [];
            }
        } catch (error) {
            console.warn('Ignoring corrupted stats storage:', error);
        }
    };

    let saveTimeout;
    const save = () => {
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            localStorage.setItem(KEY, JSON.stringify(data));
            saveTimeout = null;
        }, 500);
    };

    load();

    let checkTimeout;
    AchievementEvents.on((event, payload) => {
        if (event === 'answer_correct') {
            data.correctAnswers++;
            data.currentStreak++;
            if (data.currentStreak > data.longestStreak) data.longestStreak = data.currentStreak;
            if (payload && payload.country && !data.countriesVisited.includes(payload.country)) {
                data.countriesVisited.push(payload.country);
            }
        } else if (event === 'answer_wrong') {
            data.wrongAnswers++;
            data.currentStreak = 0;
        } else if (event === 'game_completed') {
            data.gamesPlayed++;
        }

        save();

        // Debounce achievement check to prevent lag during rapid gameplay
        if (checkTimeout) clearTimeout(checkTimeout);
        checkTimeout = setTimeout(() => {
            AchievementEngine.check();
            checkTimeout = null;
        }, 300);
    });

    return {
        get: () => data,
        reset: () => {
            if (saveTimeout) {
                clearTimeout(saveTimeout);
                saveTimeout = null;
            }
            if (checkTimeout) {
                clearTimeout(checkTimeout);
                checkTimeout = null;
            }
            data = {
                correctAnswers: 0,
                wrongAnswers: 0,
                countriesVisited: [],
                longestStreak: 0,
                currentStreak: 0,
                gamesPlayed: 0,
                xp: 0,
                level: 1
            };
            localStorage.removeItem(KEY);
            localStorage.removeItem('highScore');
            localStorage.removeItem('achievements');
            localStorage.removeItem('unlocked_achievements');
            localStorage.removeItem('person_memory');
        },
        addXP: (amount) => {
            data.xp += amount;
            const newLevel = Math.floor(Math.sqrt(data.xp / 100)) + 1;
            const leveledUp = newLevel > data.level;
            data.level = newLevel;
            save();
            return { leveledUp, level: data.level };
        }
    };
})();
