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
        if (saved) data = { ...data, ...JSON.parse(saved) };
    };

    const save = () => localStorage.setItem(KEY, JSON.stringify(data));

    load();

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
        AchievementEngine.check();
    });

    return {
        get: () => data,
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
