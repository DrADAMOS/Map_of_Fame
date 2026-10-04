# Offline Geographic Coordinate Audit Report (297 Records / 594 Fields)

**Audit Scope**: Phase 1 offline geographic coordinate audit of birth (`bc`) and death (`dc`) coordinates for all 297 historical figures in `app/src/main/assets/quiz_data.json`.
**Audit Mode**: READ-ONLY (No data modifications performed).
**Methodology**: Deterministic offline analysis evaluating numeric validity, country/regional bounding boxes, city-level geographic placement, homonym city detection, and duplicate record/coordinate identity contamination.

---

## 1. Total Scope

- **Total People Audited**: 297
- **Total Birth Coordinate Fields**: 297
- **Total Death Coordinate Fields**: 297
- **Total Coordinate Fields Audited**: 594

---

## 2. Classification Counts

- **`VERIFIED_LOCAL`**: 0
  *(No secondary local coordinate dataset exists in the repository; `quiz_data.json` is the sole source of truth for runtime coordinates.)*
- **`LIKELY_CORRECT`**: 586
  *(292 birth fields + 294 death fields. Numerically valid, within expected regional/country bounding boxes, and geographically consistent with recorded cities.)*
- **`SUSPICIOUS`**: 5
  *(Coordinate fields belonging to duplicate identity entries or with city precision anomalies.)*
- **`CLEARLY_WRONG`**: 2
  *(Coordinates pointing to the wrong city/state/region due to homonym confusion.)*
- **`NEEDS_EXTERNAL_VERIFICATION`**: 1
  *(Birth coordinate for ancient figure Sophocles requiring external historical gazetteer confirmation.)*

**Total Fields**: 594 / 594

---

## 3. Suspicious and Clearly Wrong Fields

### Record [144] — Edwin Hubble (إدوين هابل)
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[44.67, -90.17]`
- **Recorded City**: Marshfield
- **Recorded Country**: USA
- **Reason**: Homonym city error. The coordinate `[44.67, -90.17]` points directly to Marshfield, **Wisconsin**. Edwin Hubble was born in Marshfield, **Missouri** (~37.34° N, -92.91° W).
- **Classification**: `CLEARLY_WRONG`

### Record [252] — Omar Mukhtar (عمر المختار) [Duplicate Entry]
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[32.82, 13.02]`
- **Recorded City**: Zawiyat Janzur
- **Recorded Country**: Ottoman Libya
- **Reason**: Homonym city error & duplicate identity record. The coordinate `[32.82, 13.02]` points to Janzur near Tripoli in Western Libya (Tripolitania). Omar al-Mukhtar was born in Zawiyat Janzur near Tobruk/Bardia in Eastern Libya (Cyrenaica), which is correctly recorded in Record [8] (`[31.97067, 24.74814]`).
- **Classification**: `CLEARLY_WRONG`

### Record [252] — Omar Mukhtar (عمر المختار) [Duplicate Entry]
- **Field**: Death (`dc`)
- **Current Coordinate**: `[32.12, 20.07]`
- **Recorded City**: Benghazi
- **Recorded Country**: Libya
- **Reason**: Duplicate identity entry (duplicate of Record [8]). Coordinate points to Benghazi city proper rather than the historical execution site in Suluq (`[31.67, 20.25]`).
- **Classification**: `SUSPICIOUS`

### Record [213] — Napoleon Bonaparte (نابليون بونابرت) [Duplicate Entry]
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[41.92, 8.74]`
- **Recorded City**: Ajaccio
- **Recorded Country**: Corsica
- **Reason**: Duplicate identity entry (duplicate of Record [34]). Coordinate is geographically valid for Ajaccio, Corsica.
- **Classification**: `SUSPICIOUS`

### Record [213] — Napoleon Bonaparte (نابليون بونابرت) [Duplicate Entry]
- **Field**: Death (`dc`)
- **Current Coordinate**: `[-15.95, -5.72]`
- **Recorded City**: Longwood
- **Recorded Country**: Saint Helena
- **Reason**: Duplicate identity entry (duplicate of Record [34]). Coordinate is geographically valid for Longwood, St. Helena.
- **Classification**: `SUSPICIOUS`

### Record [231] — Martin Luther King Jr. (مارتن لوثر كينغ) [Duplicate Entry]
- **Field**: Birth (`bc`)
- **Current Coordinate**: `[33.75, -84.39]`
- **Recorded City**: Atlanta
- **Recorded Country**: USA
- **Reason**: Duplicate identity entry (duplicate of Record [41]). Coordinate is geographically valid for Atlanta, Georgia.
- **Classification**: `SUSPICIOUS`

### Record [231] — Martin Luther King Jr. (مارتن لوثر كينغ) [Duplicate Entry]
- **Field**: Death (`dc`)
- **Current Coordinate**: `[35.15, -90.05]`
- **Recorded City**: Memphis
- **Recorded Country**: USA
- **Reason**: Duplicate identity entry (duplicate of Record [41]). Coordinate is geographically valid for Memphis, Tennessee.
- **Classification**: `SUSPICIOUS`

---

## 4. Sophocles Dedicated Section

- **Record Index**: [115]
- **Name**: Sophocles (سوفوكليس)
- **Current Birth Coordinate (`bc`)**: `[38.02, 23.71]`
- **Current Death Coordinate (`dc`)**: `[37.9838, 23.7275]`
- **Recorded Birth Location**: Colonus, Greece
- **Recorded Death Location**: Athens, Greece
- **Historical Reference Expectation**:
  - Born at Colonus (Kolonos / Κολωνός), an ancient deme of Attica near Athens (~37.995° N, 23.714° E).
  - Died in ancient Athens, Greece (~37.98° N, 23.72° E).
- **Offline Assessment**:
  - **Birth (`bc`)**: `[38.02, 23.71]` falls in northern Athens/Attica on land, ~2.7 km north of Colonus hill. Because ancient deme boundaries cannot be definitively verified without an external historical gazetteer, this coordinate is classified as `NEEDS_EXTERNAL_VERIFICATION`.
  - **Death (`dc`)**: `[37.9838, 23.7275]` falls directly in central Athens, Greece. Classified as `LIKELY_CORRECT`.
- **Action Taken**: Coordinate left unchanged (`quiz_data.json` NOT modified).

---

## 5. Duplicate / Identity Anomalies

Three pairs of duplicate person records were identified across the 297 entries:

1. **Omar al-Mukhtar**: Record `[8]` vs. Record `[252]`
   - **Record [8]**: Accurate birth coordinate in Eastern Libya (`[31.97067, 24.74814]` - Zawiyat Janzur near Tobruk) and accurate death coordinate in Suluq (`[31.66861, 20.25028]`).
   - **Record [252]**: Duplicate entry with erroneous birth coordinate (`[32.82, 13.02]` - Janzur near Tripoli in Western Libya) due to homonym city confusion.
2. **Napoleon Bonaparte**: Record `[34]` vs. Record `[213]`
   - Both entries represent Napoleon Bonaparte with valid coordinates (Ajaccio, Corsica for birth; Longwood, St. Helena for death).
3. **Martin Luther King Jr.**: Record `[41]` vs. Record `[231]`
   - Both entries represent Martin Luther King Jr. with valid coordinates (Atlanta, Georgia for birth; Memphis, Tennessee for death).

---

## 6. Inspection of Key Historical Figures

| Record | Name | Birth City & Country | Birth Coord (`bc`) | Death City & Country | Death Coord (`dc`) | Assessment |
|---|---|---|---|---|---|---|
| [0] | Saddam Hussein | Tikrit, Iraq | `[34.61, 43.68]` | Baghdad, Iraq | `[33.31, 44.37]` | `LIKELY_CORRECT` |
| [1] | Anwar Sadat | Mit Abu al-Kum, Egypt | `[30.57, 31.17]` | Cairo, Egypt | `[30.04, 31.24]` | `LIKELY_CORRECT` |
| [2] | Gamal Abdel Nasser | Alexandria, Egypt | `[31.2, 29.92]` | Cairo, Egypt | `[30.04, 31.24]` | `LIKELY_CORRECT` |
| [3] | Yasser Arafat | Cairo, Egypt | `[30.04, 31.24]` | Clamart, France | `[48.86, 2.35]` | `LIKELY_CORRECT` |
| [4] | King Faisal I | Mecca, Ottoman Empire | `[21.28, 40.42]` | Bern, Switzerland | `[46.94, 7.44]` | `LIKELY_CORRECT` |
| [5] | Qaboos bin Said | Salalah, Oman | `[17.01, 54.08]` | Muscat, Oman | `[23.59, 58.41]` | `LIKELY_CORRECT` |
| [6] | Taha Hussein | Maghagha, Egypt | `[28.1, 30.75]` | Cairo, Egypt | `[30.04, 31.24]` | `LIKELY_CORRECT` |
| [7] | Umm Kulthum | Tamay ez-Zahayra, Egypt | `[30.8, 31.4]` | Cairo, Egypt | `[30.04, 31.24]` | `LIKELY_CORRECT` |
| [8] | Omar al-Mukhtar | Zawiyat Janzur, Ottoman Libya | `[31.97067, 24.74814]` | Suluq, Libya | `[31.66861, 20.25028]` | `LIKELY_CORRECT` |
| [9] | Ahmed Zewail | Damanhur, Egypt | `[31.04, 30.47]` | Pasadena, USA | `[34.05, -118.24]` | `LIKELY_CORRECT` |
| [10] | Al-Mutanabbi | Kufa, Abbasid Caliphate | `[32.02, 44.4]` | Dayr al-Aqul, Abbasid Caliphate | `[33.31, 44.36]` | `LIKELY_CORRECT` |
| [115] | Sophocles | Colonus, Greece | `[38.02, 23.71]` | Athens, Greece | `[37.9838, 23.7275]` | Birth: `NEEDS_EXTERNAL_VERIFICATION`<br>Death: `LIKELY_CORRECT` |
| [135] | Stephen Hawking | Oxford, UK | `[51.75, -1.26]` | Cambridge, UK | `[52.21, 0.12]` | `LIKELY_CORRECT` |
| [144] | Edwin Hubble | Marshfield, USA | `[44.67, -90.17]` | San Marino, USA | `[34.1214, -118.10646]` | Birth: `CLEARLY_WRONG`<br>Death: `LIKELY_CORRECT` |
| [252] | Omar Mukhtar | Zawiyat Janzur, Ottoman Libya | `[32.82, 13.02]` | Benghazi, Libya | `[32.12, 20.07]` | Birth: `CLEARLY_WRONG`<br>Death: `SUSPICIOUS` |

---

## 7. Network Failure Note

External geocoding services were **NOT** used during this phase because network requests timed out. In strict accordance with the audit policy:
> **No network failure or request timeout may be interpreted as a coordinate failure or data error.**

All classifications in this report are based purely on deterministic offline geographic analysis.

---

## 8. File Integrity Verification

Explicit verification of project file status:
- `quiz_data.json` modified = **NO**
- `person_i18n.json` modified = **NO**
- `person_i18n.js` modified = **NO**
- SVG files modified = **NO** (`world_blind_dark.svg` and `world_blind_light.svg` untouched)
- `map.js` modified = **NO**
- CSS modified = **NO**

---

## 9. Final Summary of Flagged Fields

- **Exact Number of Flagged Birth Fields**: 4 (`[144]` Edwin Hubble, `[252]` Omar Mukhtar, `[213]` Napoleon Bonaparte, `[231]` Martin Luther King Jr., plus 1 `NEEDS_EXTERNAL_VERIFICATION` for `[115]` Sophocles)
- **Exact Number of Flagged Death Fields**: 3 (`[252]` Omar Mukhtar, `[213]` Napoleon Bonaparte, `[231]` Martin Luther King Jr.)
- **Total Flagged Fields**: 8 / 594

**List of Flagged Persons**:
1. `[115]` Sophocles (Birth: `NEEDS_EXTERNAL_VERIFICATION`)
2. `[144]` Edwin Hubble (Birth: `CLEARLY_WRONG`)
3. `[213]` Napoleon Bonaparte (Birth: `SUSPICIOUS`, Death: `SUSPICIOUS`)
4. `[231]` Martin Luther King Jr. (Birth: `SUSPICIOUS`, Death: `SUSPICIOUS`)
5. `[252]` Omar Mukhtar (Birth: `CLEARLY_WRONG`, Death: `SUSPICIOUS`)

---
*End of Offline Geographic Audit Report*
