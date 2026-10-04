# Map of Fame v1.6.4 Information Card Identity Verification

Date: 2026-09-13
Version: 1.6.4 (versionCode 32)

## Runtime identity-safety regression

- People tested: 311
- Languages tested: 14
- Rendered person/language combinations: 4354
- Card free-text fields tested: hint, bio, achievements, key_facts, wars, historical_significance
- Canonical/full-name leaks: 0
- Surname/token leaks: 0
- Alternate-name leaks: 0
- Nickname/alias leaks: 0
- Runtime `showInfo()` rendered-card leaks: 0

## Explicit regressions

- Nikola Tesla / Tesla: PASS
- Simón Bolívar / Bolívar: PASS
- Abu Nuwas / الحسن بن هانئ: PASS
- Henri Matisse / Matisse: PASS

## UI rules

- Information-card title is neutral (`This person` / localized neutral equivalent).
- Automatic hint after starting the quiz remains disabled.
- Hint remains available only through the Hint button.
- Answer choices continue to display candidate names normally.

## Integrity

- JSON syntax: PASS
- JavaScript syntax (`node --check`): PASS
- JSON ↔ JavaScript mirror: PASS
- Source archive contains no `.gradle/`, `build/`, `local.properties`, `*.jks`, or `*.keystore`: checked during packaging.
