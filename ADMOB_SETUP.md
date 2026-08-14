# Map of Fame AdMob setup

Configured App ID:
`ca-app-pub-3676225489502432~1276974483`

Production ad units:
- Banner: `ca-app-pub-3676225489502432/3534688342`
- Interstitial: `ca-app-pub-3676225489502432/2593925587`
- Rewarded interstitial: `ca-app-pub-3676225489502432/1280843912`

The source currently uses Google test ad unit IDs while `USE_TEST_ADS` is true in `MainActivity.kt`. Set it to false only after the app has been fully tested and before the production release build.

The current Rewarded unit in AdMob is a **Rewarded interstitial**, not a standard opt-in Rewarded ad. It is therefore not wired to the Hint button. Create a separate standard Rewarded ad unit if you want the player to explicitly watch an ad for a hint.


Rewarded ad unit configured: ca-app-pub-3676225489502432/4544517681. The Hint button requests a rewarded ad; the hint is granted after the reward callback. Test ads remain enabled during development.
