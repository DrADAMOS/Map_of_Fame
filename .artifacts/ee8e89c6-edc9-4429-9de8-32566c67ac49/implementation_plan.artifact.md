# Fix Build Resolution Errors (Offline Mode)

The build is failing because Gradle is currently set to **Offline Mode**, and the required dependency versions (specifically `compose-bom:2025.02.00` and `play-services-maps:19.0.0`) are not yet available in your local cache.

## User Action Required

> [!IMPORTANT]
> **Disable Offline Mode in Android Studio:**
> 1. Open the **Gradle** tool window (usually on the right side of Android Studio).
> 2. Click the **Toggle Offline Mode** icon (it looks like a cloud with a slash or a Wi-Fi signal icon) to disable it.
> 3. Click **Sync Project with Gradle Files** (elephant icon in the toolbar).

## Proposed Changes

While the primary fix is disabling offline mode, I will also update your `:app/build.gradle.kts` to consistently use the **Version Catalog** (`libs.versions.toml`) instead of hardcoded strings. This makes the project cleaner and easier to manage.

### `:app` Module

#### [MODIFY] [build.gradle.kts](file:///C:/Users/ADAMOS/My Android Projects/MapofFame/app/build.gradle.kts)
- Replace hardcoded Compose and Google Maps dependencies with references from `libs.versions.toml`.

## Verification Plan

### Manual Verification
- After you disable Offline Mode and sync, I will run a build to confirm all dependencies are resolved.
- Command: `gradle_build(":app:assembleDebug")`
