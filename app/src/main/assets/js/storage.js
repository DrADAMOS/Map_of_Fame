const Storage = (() => {
    const safeParse = (raw, fallback) => {
        if (!raw) return fallback;
        try {
            const parsed = JSON.parse(raw);
            return parsed ?? fallback;
        } catch (error) {
            console.warn('Ignoring corrupted localStorage value:', error);
            return fallback;
        }
    };

    return {
        saveSettings: (settings) => {
            localStorage.setItem('game_settings', JSON.stringify(settings));
        },
        getSettings: () => {
            // English is the first-launch default; a user's saved language choice is preserved.
            const defaults = { lang: 'en', theme: 'dark', lastMode: 'all', lastDiff: 'easy' };
            const saved = safeParse(localStorage.getItem('game_settings'), {});
            return { ...defaults, ...(saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {}) };
        },
        updateHighScore: (score) => {
            const high = Number(localStorage.getItem('highScore')) || 0;
            const numericScore = Number(score) || 0;
            if (numericScore > high) {
                localStorage.setItem('highScore', String(numericScore));
                return true;
            }
            return false;
        },
        getHighScore: () => Number(localStorage.getItem('highScore')) || 0,
        unlockAchievement: (id) => {
            const saved = safeParse(localStorage.getItem('achievements'), []);
            const unlocked = Array.isArray(saved) ? saved : [];
            if (!unlocked.includes(id)) {
                unlocked.push(id);
                localStorage.setItem('achievements', JSON.stringify(unlocked));
                return true;
            }
            return false;
        },
        getAchievements: () => {
            const saved = safeParse(localStorage.getItem('achievements'), []);
            return Array.isArray(saved) ? saved : [];
        },
        recordLearning: (person, correct) => {
            if (!person || !person.name) return null;
            const memory = safeParse(localStorage.getItem('person_memory'), {});
            const store = memory && typeof memory === 'object' && !Array.isArray(memory) ? memory : {};
            const key = person.name_en || person.name;
            const old = store[key] || { seen: 0, correct: 0, wrong: 0, mastery: 0, streak: 0, status: 'جديدة' };
            old.seen += 1;
            if (correct) { old.correct += 1; old.streak = (old.streak || 0) + 1; } else { old.wrong += 1; old.streak = 0; }
            old.mastery = Math.max(0, Math.min(100, Math.round((old.correct / old.seen) * 100)));
            old.lastSeen = Date.now();
            if (old.streak >= 2 && old.mastery >= 75) old.status = 'MASTERED';
            else if (!correct) old.status = 'FAILED';
            else old.status = 'REVIEW';
            old.name = person.name;
            old.name_en = person.name_en || person.name;
            store[key] = old;
            localStorage.setItem('person_memory', JSON.stringify(store));
            return old;
        },
        getPersonMemory: (person) => {
            if (!person || !person.name) return null;
            const memory = safeParse(localStorage.getItem('person_memory'), {});
            return memory[(person.name_en || person.name)] || null;
        },
        statusLabel: (status, lang = 'en') => {
            const labels = {
                MASTERED: { ar: 'متقنة', en: 'Mastered' },
                REVIEW: { ar: 'تحتاج مراجعة', en: 'Review' },
                FAILED: { ar: 'أخطأت بها', en: 'Failed' },
                'متقنة': { ar: 'متقنة', en: 'Mastered' },
                'تحتاج مراجعة': { ar: 'تحتاج مراجعة', en: 'Review' },
                'أخطأت بها': { ar: 'أخطأت بها', en: 'Failed' }
            };
            return (labels[status] && labels[status][lang]) || (lang === 'en' ? 'Review' : 'تحتاج مراجعة');
        },
        markMasterySynced: (person) => {
            if (!person || !person.name) return null;
            const memory = safeParse(localStorage.getItem('person_memory'), {});
            const key = person.name_en || person.name;
            const current = memory[key];
            if (!current) return null;
            current.syncedAt = Date.now();
            current.masteryStatus = current.status;
            memory[key] = current;
            localStorage.setItem('person_memory', JSON.stringify(memory));
            return current;
        },
        getLearningSummary: () => {
            const memory = safeParse(localStorage.getItem('person_memory'), {});
            const values = Object.values(memory && typeof memory === 'object' ? memory : {});
            const mastered = values.filter(x => x.status === 'MASTERED' || x.status === 'متقنة' || x.mastery >= 75).length;
            const failed = values.filter(x => x.status === 'FAILED' || x.status === 'أخطأت بها').length;
            const review = values.filter(x => (x.status === 'REVIEW' || x.status === 'تحتاج مراجعة') && x.status !== 'FAILED').length;
            return { learned: values.length, mastered, review, failed, activeReview: review + failed };
        },
        getReviewCharacters: (all) => {
            const memory = safeParse(localStorage.getItem('person_memory'), {});
            if (!Array.isArray(all)) return [];
            return all.filter(person => {
                const key = person.name_en || person.name;
                const m = memory && typeof memory === 'object' ? memory[key] : null;
                return m && (m.status === 'MASTERED' || m.status === 'متقنة') === false && (m.status === 'REVIEW' || m.status === 'FAILED' || m.status === 'تحتاج مراجعة' || m.status === 'أخطأت بها' || m.mastery < 75);
            });
        }
    };
})();
