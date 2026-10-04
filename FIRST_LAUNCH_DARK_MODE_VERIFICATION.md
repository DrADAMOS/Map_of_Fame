# First Launch Dark Mode Verification

- Default when `theme_mode` is absent: `dark` (`viewModel.setTheme(true)`).
- Existing saved `theme_mode` is preserved.
- WebView default remains dark (`Storage.getSettings()` defaults to `theme: 'dark'`).
- Start HTML applies a dark background immediately to prevent a white flash.
- English first-launch default remains unchanged (`lang: 'en'`).

Expected behavior:
1. Fresh install / cleared app data -> dark mode.
2. User switches to light -> saved as light.
3. Relaunch -> light remains.
4. User switches back -> dark remains.
