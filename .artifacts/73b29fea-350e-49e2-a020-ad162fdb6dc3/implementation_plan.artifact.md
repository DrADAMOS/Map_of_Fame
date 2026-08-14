# Implementation Plan - Event-Driven Achievement & Progression System

This plan details the implementation of a professional, modular achievement system for "Map of Fame" using an event-driven architecture.

## User Review Required

> [!IMPORTANT]
> **Decoupled Architecture**: The game logic will now only emit events (e.g., `Events.emit('answer_correct')`). The achievement system will listen to these events independently, making the codebase much cleaner and more maintainable.
>
> **Stats Migration**: I will consolidate all local storage keys related to player progress into a single `Stats` object to track over 15 metrics.

## Proposed Changes

### 1. Core Event System
#### [NEW] [achievement_events.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_events.js)
- A lightweight event emitter to bridge the game loop and the achievement engine.

### 2. Data & Statistics
#### [NEW] [achievement_data.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_data.js)
- Fully data-driven definitions with conditions (`target`, `metric`) and tiers (Bronze to Legendary).

#### [NEW] [stats.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/stats.js)
- Centralized tracking of: `correctAnswers`, `wrongAnswers`, `countriesVisited`, `longestStreak`, `averageAnswerTime`, `perfectGames`, `xp`, `level`, etc.

### 3. Achievement Logic & Persistence
#### [NEW] [achievement_engine.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_engine.js)
- Listens to events, updates stats, and checks against achievement definitions.

#### [NEW] [achievement_storage.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_storage.js)
- Saves unlocked status, unlock dates, and current progress per achievement.

#### [NEW] [achievement_rewards.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_rewards.js)
- XP calculation and level-up logic.

### 4. UI & High-End Visuals
#### [NEW] [achievement_ui.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/achievements/achievement_ui.js)
- **Achievement Dashboard**: A full-screen page with progress bars (`410 / 500 [████░] 82%`).
- **Unlock Toast**: Animated top-sliding notification with glow, sound, and confetti.
- **Stats Dashboard**: Summary of all player metrics.

#### [MODIFY] [style.css](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/css/style.css)
- Rarity colors, shimmer effects, and progress bar animations.

### 5. Integration
#### [MODIFY] [quiz.js](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/js/quiz.js)
- Inject `AchievementEvents.emit()` into `checkAns()`, `endGame()`, and `startGame()`.

#### [MODIFY] [game.html](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/src/main/assets/game.html)
- Add Achievement button to the start screen.
- Load the new modular scripts in the correct dependency order.

## Verification Plan

### Manual Verification
- **XP Progression**: Verify that answering a question correctly increases XP and eventually levels up the player.
- **Progress Tracking**: Check the Achievement Dashboard and ensure the progress bar accurately reflects the stats.
- **Unlock Sequence**: Achieve 5 correct answers in a row to verify the "Sharp Eye" unlock animation and sound.
- **Persistence**: Close the app and verify that stats and unlocked achievements are correctly restored from LocalStorage.
