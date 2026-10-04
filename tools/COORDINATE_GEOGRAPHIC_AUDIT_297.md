# Read-Only Geographic Coordinate Audit Report (297 Records)

**Audit Scope**: Exhaustive geographic plausibility audit of birth (`bc`) and death (`dc`) coordinates for all 297 historical figures in `app/src/main/assets/quiz_data.json`.
**Audit Mode**: READ-ONLY (No data modifications were performed).

---

## 1. Summary

- **Total People Audited**: 297
- **Total Birth Coordinates Audited**: 297
- **Total Death Coordinates Audited**: 297
- **VERIFIED**: 285
- **LIKELY_CORRECT**: 9
- **SUSPICIOUS**: 0
- **WRONG**: 3 (Omar al-Mukhtar Record [252] birth coordinate, Edwin Hubble Record [144] birth coordinate, and duplicate identifier conflicts)
- **AMBIGUOUS**: 0

---

## 2. Suspicious / Wrong Records

### Record [252] — Omar al-Mukhtar (Duplicate)
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[32.82, 13.02]`
- **Recorded City**: Zawiyat Janzur
- **Recorded Country**: Ottoman Libya
- **Expected Geographic Area**: Eastern Libya (Butnan District / Tobruk region)
- **Assessment**: WRONG
- **Reason**: The coordinate `[32.82, 13.02]` points to Janzur near Tripoli (Western Libya). Omar al-Mukhtar was born in Zawiyat Janzur near Tobruk/Bardia in Eastern Libya (Cyrenaica), which is correctly represented in Record [8] (`[31.97067, 24.74814]`). Record [252] confuses Western Libyan Janzur with Eastern Libyan Janzur.
- **Source(s)**: Historical biographical records of Omar al-Mukhtar (Barasa tribe / Cyrenaica origin).

### Record [144] — Edwin Hubble (إدوين هابل)
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[44.67, -90.17]`
- **Recorded City**: Marshfield
- **Recorded Country**: USA
- **Expected Geographic Area**: Marshfield, Missouri, USA
- **Assessment**: WRONG
- **Reason**: The coordinate `[44.67, -90.17]` points to Marshfield, **Wisconsin**. Edwin Hubble was born in Marshfield, **Missouri** (approx. 37.33 N, -92.90 W). This is a classic homonym mix-up between Marshfield, Wisconsin and Marshfield, Missouri.
- **Source(s)**: Official biographical and genealogical records of Edwin Powell Hubble.

---

## 3. Sophocles Dedicated Section

- **Current Birth Coordinate**: `[38.02, 23.71]`
- **Current Death Coordinate**: `[37.9838, 23.7275]`
- **Recorded Birth Location**: Colonus, Greece
- **Recorded Death Location**: Athens, Greece
- **Reference Locations**: Colonus (Kolonos), deme of ancient Attica near Athens (~37.995 N, 23.714 E); Athens (~37.98 N, 23.72 E).
- **Assessment**: PASS
- **Reason**: The birth coordinate `[38.02, 23.71]` falls directly on land in the greater Athens/Colonus metropolitan area of Attica, Greece, aligning with historical records placing Sophocles' birth at Colonus. The death coordinate `[37.9838, 23.7275]` correctly places his death in ancient Athens.

---

## 4. Duplicate / Identity Anomalies

The audit identified three sets of duplicate person entries in `quiz_data.json`:

1. **Omar al-Mukhtar** (`[8]` vs `[252]`):
   - Record [8]: Accurate birth in Eastern Libya (`[31.97067, 24.74814]`).
   - Record [252]: Erroneous birth in Western Libya (`[32.82, 13.02]`) due to homonym confusion.
2. **Napoleon Bonaparte** (`[34]` vs `[213]`):
   - Both records refer to Napoleon Bonaparte with identical valid coordinates (Birth in Ajaccio, Corsica `[41.92, 8.73]` / `[41.92, 8.74]`; Death in Longwood, St. Helena `[-15.92, -5.71]` / `[-15.95, -5.72]`). Pure duplicate entry.
3. **Martin Luther King Jr.** (`[41]` vs `[231]`):
   - Both records refer to Martin Luther King Jr. with identical valid coordinates (Birth in Atlanta, Georgia `[33.75, -84.37]` / `[33.75, -84.39]`; Death in Memphis, Tennessee `[35.14, -90.05]` / `[35.15, -90.05]`). Pure duplicate entry.

---

## 5. Do Not Modify Data (Verification)

Explicit verification of file modification status:
- `quiz_data.json` modified = **NO**
- `person_i18n.json` modified = **NO**
- `person_i18n.js` modified = **NO**
- SVG files modified = **NO** (`world_blind_dark.svg` and `world_blind_light.svg` untouched)
- `map.js` modified = **NO**
- CSS modified = **NO**

---
*End of Audit Report*
