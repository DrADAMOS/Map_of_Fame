const AchievementEngine = (() => {
    return {
        check: () => {
            const stats = Stats.get();
            const unlocked = AchievementStorage.getUnlocked();

            ACHIEVEMENT_DATA.forEach(ach => {
                if (unlocked[ach.id]) return;

                let currentValue = 0;
                if (ach.condition === 'countriesVisited') {
                    currentValue = stats.countriesVisited.length;
                } else {
                    currentValue = stats[ach.condition];
                }

                if (currentValue >= ach.target) {
                    AchievementStorage.saveUnlock(ach.id);
                    const rewardResult = Stats.addXP(ach.reward);
                    AchievementUI.notify(ach, rewardResult);
                }
            });
        }
    };
})();
