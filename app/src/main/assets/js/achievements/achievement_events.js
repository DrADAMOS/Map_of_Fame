const AchievementEvents = (() => {
    const listeners = [];

    return {
        on: (callback) => listeners.push(callback),
        emit: (event, data) => {
            console.log(`Event Emitted: ${event}`, data);
            listeners.forEach(listener => {
                try {
                    listener(event, data);
                } catch (e) {
                    console.error(`Error in Achievement listener for ${event}:`, e);
                }
            });
        }
    };
})();
