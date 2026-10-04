# Light Mode Final Fix Audit

- Light Mode only: PASS
- Actual information-card `learning-extra-row` text explicitly forced to `#252525`
- Learning cards explicitly forced to `#FFFFFF`
- Accent labels/icons: `#9A5B12`
- Dark Mode changed by this pass: NO
- Data changed by this pass: NO
- Coordinates changed by this pass: NO

## Coordinate spot-check
- Pyrrhus of Epirus birth: `[39.155, 20.9899]`
- Horatio Kitchener death: `[59.11706, -3.39566]`

The earlier visual fix targeted `.ach-card`, but the screenshot's pale information content is generated as `.learning-extra-row`. This pass fixes that actual selector.
