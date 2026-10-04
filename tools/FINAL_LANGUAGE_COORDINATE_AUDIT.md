# Final Language + Coordinate Audit

- People: **297**
- Coordinate records: **594**
- LAND: **589**
- OPEN_WATER: **0**
- INLAND_WATER: **4**
- ICE_SHELF: **1**
- UNKNOWN: **0**

## Language policy
- Non-English person fields that are exact English copies are hidden instead of falling back to English.
- Arabic metadata containing Latin text is hidden instead of mixing languages.
- Recall questions no longer inject city/country/role metadata; they use only the selected-language hint/bio.
- UI locale packs now contain the missing settings/about/rate/share/reset/error labels for all 14 supported locales.

## Coordinate integrity
- `quiz_data.json` and `js/constants.js` contain 297 matching people and matching birth/death coordinates.
- Pyrrhus birth: `[39.155, 20.9899]`.
- Horatio Kitchener death: `[59.11706, -3.39566]`.
- Natural Earth 10m land/ocean/lakes/minor-islands/ice-shelf data was used for a full 594-point spatial classification.

## Non-land classifications

- Rosa Parks — death: `INLAND_WATER` at `[42.33, -83.05]`
- René Descartes — death: `INLAND_WATER` at `[59.33, 18.07]`
- Robert Falcon Scott — death: `ICE_SHELF` at `[-79.48139, 169.36778]`
- Alfred Nobel — birth: `INLAND_WATER` at `[59.33, 18.07]`
- Gabriele D'Annunzio — death: `INLAND_WATER` at `[45.62, 10.56]`

## Important interpretation
These spatial classifications are not by themselves proof that a historical coordinate is wrong. Coastal cities, harbours, shipwrecks and historical sites can legitimately fall outside a land polygon. No additional coordinate was silently moved based only on land/water classification.

## JS syntax
- `quiz.js`: **PASS**
- `ui.js`: **PASS**
- `i18n_languages.js`: **PASS**
- `map.js`: **PASS**