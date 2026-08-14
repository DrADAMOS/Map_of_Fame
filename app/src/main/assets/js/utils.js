const Utils = {
    vibrate: (ms) => {
        if (window.Android && Android.vibrate) {
            Android.vibrate(ms);
        }
    },
    share: (text) => {
        if (window.Android && Android.share) {
            Android.share(text);
        }
    },
    random: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
    shuffle: (array) => [...array].sort(() => Math.random() - 0.5),
    formatYear: (year, t) => {
        return Math.abs(year) + " " + (year > 0 ? t.ce : t.bce);
    }
};
