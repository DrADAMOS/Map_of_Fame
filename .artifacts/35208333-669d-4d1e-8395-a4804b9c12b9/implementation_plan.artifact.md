# Implementation Plan - Fix Kotlin Extension Conflict (AGP 9.0+)

The project is using Android Gradle Plugin (AGP) 9.3.0, which includes "built-in Kotlin support" enabled by default. This built-in support automatically applies the Kotlin configuration to Android modules. Manually applying the `org.jetbrains.kotlin.android` plugin (or even having it in the `plugins` block with `apply false` in some cases with newer AGP versions) can cause a conflict with the `kotlin` extension name.

## Proposed Changes

### 1. Remove Kotlin Android Plugin References
Since AGP 9.0+ handles Kotlin compilation automatically, the `org.jetbrains.kotlin.android` plugin is no longer required and causes conflicts.

#### [MODIFY] [libs.versions.toml](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/gradle/libs.versions.toml)
- Remove the `kotlin-android-plugin` entry from the `[plugins]` section.

#### [MODIFY] [build.gradle.kts](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/build.gradle.kts) (root)
- Remove `alias(libs.plugins.kotlin.android.plugin) apply false` from the `plugins` block.

#### [MODIFY] [app/build.gradle.kts](file:///C:/Users/ADAMOS/My%20Android%20Projects/MapofFame/app/build.gradle.kts)
- Ensure `alias(libs.plugins.kotlin.android.plugin)` is not present in the `plugins` block. (Based on current file state, it seems to be already removed, but I will verify and ensure consistency).

### 2. Verify `kotlin-compose-plugin`
- The `org.jetbrains.kotlin.plugin.compose` plugin is still required for the Compose compiler (starting with Kotlin 2.0). I will keep it as it is specifically for the Compose compiler and shouldn't conflict with the basic Kotlin extension if applied correctly.

## Verification Plan

### Automated Tests
- Run Gradle sync (simulated by `./gradlew help`).
- Verify Kotlin compilation: `./gradlew :app:compileDebugKotlin`.

### Manual Verification
- Check if the "Cannot add extension with name 'kotlin'" error is resolved in Android Studio.
