# Card / Hint Behavior Verification

- Information card remains the pre-question learning surface.
- The automatic person-specific hint is disabled after `beginRecallChallenge()`.
- `questionPrompt` contains only the generic localized question prompt.
- `hintTxt` is empty/hidden until the player explicitly presses the hint button.
- `doHint()` / `grantHint()` remain intact for opt-in hints.
- No person-specific hint/bio is injected into `questionPrompt`.
