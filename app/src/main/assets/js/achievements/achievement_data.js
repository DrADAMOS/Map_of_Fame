const ACHIEVEMENT_DATA = [
    {
        id: "scholar_1",
        condition: "correctAnswers",
        target: 10,
        title: { ar: "باحث تاريخي I", en: "Scholar I" },
        desc: { ar: "أجب على 10 أسئلة بشكل صحيح", en: "Answer 10 questions correctly." },
        reward: 100,
        tier: "Bronze",
        icon: "book"
    },
    {
        id: "scholar_2",
        condition: "correctAnswers",
        target: 50,
        title: { ar: "باحث تاريخي II", en: "Scholar II" },
        desc: { ar: "أجب على 50 سؤالاً بشكل صحيح", en: "Answer 50 questions correctly." },
        reward: 250,
        tier: "Silver",
        icon: "book-open"
    },
    {
        id: "explorer_1",
        condition: "countriesVisited",
        target: 5,
        title: { ar: "مكتشف I", en: "Explorer I" },
        desc: { ar: "زر 5 دول مختلفة", en: "Visit 5 different countries." },
        reward: 150,
        tier: "Bronze",
        icon: "compass"
    },
    {
        id: "streak_1",
        condition: "longestStreak",
        target: 5,
        title: { ar: "عين الصقر I", en: "Sharp Eye I" },
        desc: { ar: "أجب على 5 أسئلة متتالية بشكل صحيح", en: "Get a 5-correct answer streak." },
        reward: 200,
        tier: "Bronze",
        icon: "eye"
    }
];
