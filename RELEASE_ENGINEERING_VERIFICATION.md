# Release Engineering Verification

## Release configuration
- versionCode: 32
- versionName: 1.6.4
- targetSdk: 36
- compileSdk: 37
- release minification: enabled
- release resource shrinking: enabled

## Repository hygiene
- `.gradle/` ignored
- `**/.gradle/` ignored
- Gradle lock files under `.gradle/` ignored
- `**/build/` ignored
- `local.properties` ignored
- `keystore.properties` ignored
- `*.jks` and `*.keystore` ignored
- no local keystore or local.properties present in release archive
- no `.gradle` or `build` directory present in release archive

## WebView / bridge
- WebView debugging is gated by `BuildConfig.DEBUG`; production is disabled.
- Local content is served through `WebViewAssetLoader`.
- Direct file/content access is disabled.
- Cleartext traffic is disabled in the manifest.
- WebView navigation is restricted to the bundled asset origin.
- Wikipedia bridge URLs require HTTPS and an approved Wikipedia host/language.
- External bridge URLs require HTTPS, no userinfo/explicit port, and `play.google.com` host.
- URL inputs are length-limited to 2048 characters and reject control characters.
- Vibration input is clamped to 1..2000 ms.
- Share text is trimmed and capped at 4000 characters.

## R8 / ProGuard
- The JavaScript bridge class is kept.
- All `@JavascriptInterface` methods are kept.
- App fields are retained for reflective/native JSON model compatibility.
- Current game JSON is parsed in JavaScript; no Gson/Kotlinx native model keep rules are required by the current implementation.

## Signing
- Release signing reads from `MAP_OF_FAME_*` environment variables or root `keystore.properties`.
- Signing credentials are not hardcoded.
- Signing files are excluded from Git and release archives.

## Build execution limitation
A full Gradle `clean/test/lint/bundleRelease` execution was not performed in this packaging environment because the Gradle 9.6.0 distribution is not installed locally and external dependency download is unavailable. The project is therefore packaged without claiming a false Gradle build PASS.
