# Strict Card Identity Verification — 2026-09-13

Scope: learning/information card and pre-answer hint.

- People: 311
- Languages: 14
- Card field values checked: 39541
- Canonical/localized identity leaks after runtime sanitization: 0
- Explicit nickname/alternate-name marker leaks after runtime sanitization: 0
- JSON ↔ JavaScript mirror: PASS
- Constants dataset records: 311

## Regression — Abu Nuwas

Input biography:
`كان أبو نواس الحسن بن هانئ شاعرًا عباسيًا من أشهر شعراء القرن الثاني الهجري.`

Expected rendered result:
`كان شاعرًا عباسيًا من أشهر شعراء القرن الثاني الهجري.`

The card must not display the canonical answer, formal name, surname-only form, or nickname. Names remain in the underlying answer dataset because the quiz requires them for answer/options; the identity protection is applied at the card rendering boundary.

## Initials protection

Sentence splitting protects forms such as `John F. Kennedy`, `T. E. Lawrence`, Arabic initials, and Roman numerals so identity matching cannot be bypassed by punctuation-based sentence splitting.
