# Fix Dependency Resolution and Offline Mode Issues

The project is experiencing build failures because Gradle is unable to resolve certain dependencies (specifically `play-services-maps` and `compose-bom`) while in "offline mode". Additionally, there is a mismatch between the version catalog (`libs.versions.toml`) and the hardcoded dependencies in `app/build.gradle.kts`.

## User Review Required

> [!IMPORTANT]
> The error message indicates that your IDE/Gradle is running in **Offline Mode**. You MUST disable this setting to allow Gradle to download the required dependencies.
>
> To disable Offline Mode:
> 1. Go to **File > Settings** (on Windows/Linux) or **Android Studio > Settings** (on macOS).
> 2. Navigate to **Build, Execution, Deployment > Build Tools > Gradle**.
> 3. Uncheck **Offline work** (if visible) or ensure the "Offline Mode" toggle in the Gradle tool window (usually on the right side of the IDE) is turned **OFF**.

## Proposed Changes

### [Component Name] Dependency Management

I will synchronize the dependencies between the version catalog and the build file, and update them to the latest stable versions to ensure they are correctly resolvable.

#### [MODIFY] [libs.versions.toml](file:///C:/Users/ADAMOS/My Android Projects/MapofFame/gradle/libs.versions.toml)
- Update `compose-bom` to `2026.06.01`.
- Update `play-services-maps` to `20.0.0`.
- Update `google-maps-compose` to `8.4.0`.

#### [MODIFY] [app/build.gradle.kts](file:///C:/Users/ADAMOS/My Android Projects/MapofFame/app/build.gradle.kts)
- Replace hardcoded dependency strings with references from the version catalog (`libs`).
- Ensure consistent use of the Compose BOM for all Compose-related dependencies.

## Verification Plan

### Automated Tests
- Run `./gradlew clean build` (or use the `gradle_build` tool) to ensure dependencies are resolved and the project builds successfully.
- Trigger a Gradle Sync to verify the IDE correctly indexes the new versions.

### Manual Verification
- Verify that the error "Could Not Resolve..." no longer appears in the Build output.
