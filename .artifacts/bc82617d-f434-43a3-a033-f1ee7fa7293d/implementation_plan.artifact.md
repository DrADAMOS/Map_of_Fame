# Fix Build Error: Dependency Resolution in Offline Mode

The project is currently failing to build because Gradle is in **offline mode** and cannot resolve several dependencies, including `com.google.android.gms:play-services-maps:19.0.0` and `androidx.compose:compose-bom:2025.02.00`. These dependencies are missing from the local Gradle cache.

Additionally, the `app/build.gradle.kts` file contains hardcoded dependency versions that should ideally be managed through the Version Catalog (`libs.versions.toml`) to ensure consistency.

## User Review Required

> [!IMPORTANT]
> The primary cause of this error is that Gradle is configured to run in **Offline Mode** while trying to fetch new or uncached dependencies. You will need to disable Offline Mode in your IDE settings to allow Gradle to download these files.

## Proposed Changes

### Build Configuration & Dependency Management

#### [MODIFY] [libs.versions.toml](file:///C:/Users/ADAMOS/My Android Projects/MapofFame/gradle/libs.versions.toml)
- Update `play-services-maps` and other related dependencies to their latest stable versions.
- Ensure all failing dependencies have proper definitions in the catalog.

#### [MODIFY] [app/build.gradle.kts](file:///C:/Users/ADAMOS/My Android Projects/MapofFame/app/build.gradle.kts)
- Refactor the `dependencies` block to use `libs.` references instead of hardcoded strings for Compose and Google Maps dependencies.
- This will unify the version management and make the project more maintainable.

## Verification Plan

### Automated Tests
- Run `./gradlew :app:assembleDebug` to verify that the build configuration is correct.
- Note: This may still fail if offline mode remains enabled, but the error message will confirm if the configuration is resolved.

### Manual Verification
- I will instruct you on how to disable **Offline Mode** in Android Studio:
    1. Open the **Gradle** tool window (usually on the right side of the IDE).
    2. Click on the **Toggle Offline Mode** button (it looks like a cloud with a slash or a wifi icon with a line through it) to disable it.
    3. Perform a **Gradle Sync**.
