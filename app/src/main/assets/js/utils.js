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
        const num = Number(year);
        if (!Number.isFinite(num)) return String(year);
        return Math.abs(num) + " " + (num < 0 ? t.bce : t.ce);
    },
    // ISO dates ending in -01-01 are year-only estimates, so never expose 1 January as exact.
    formatDisplayYear: (dateValue, fallbackYear, t) => {
        const match = typeof dateValue === 'string' ? dateValue.match(/^(-?\d{1,4})(?:-\d{2}-\d{2})?$/) : null;
        const year = match ? Number(match[1]) : fallbackYear;
        return Utils.formatYear(Number.isFinite(year) ? year : fallbackYear, t);
    }
};
