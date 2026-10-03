# Module 4 Downloadable: Mortality and Sanitation Audit Log

**Commercial Heliculture Masterclass · Snail World (snailworld.org)**
**Format:** spreadsheet (one tab per log) with a matching printable A4 version for wall clipboards. Keep records for at least 2 years.

---

## Log 1: Daily Mortality Register (one row per unit per day)

| Col | Field | Entry / formula |
|---|---|---|
| A | Date | dd/mm/yyyy |
| B | Pen / unit ID | e.g. G-03 |
| C | Stage | Hatchling / Grower / Breeder / Quarantine |
| D | Opening live stock count | = previous day's closing count (H) |
| E | Dead today | count |
| F | Culled today (moribund, humanely dispatched) | count |
| G | Removed or moved (sold, transferred) | count |
| H | Closing live stock count | `=D-E-F-G` |
| I | Daily mortality % | `=IF(D>0,(E+F)/D*100,0)` |
| J | 7-day average mortality % | `=AVERAGE(I over last 7 rows for this unit)` |
| K | Baseline mortality % (per unit, set after the first cycle) | input |
| L | Status | `=IF(OR(I>=5*K, cluster="Y"),"OUTBREAK",IF(J>=2*K,"ALERT","Normal"))` |
| M | Clustered deaths in one box or area? | Y / N |
| N | Clinical signs observed | codes (see below) |
| O | Action taken | free text |
| P | Initials | |

**Clinical sign codes:**

| Code | Sign | Likely causes to investigate |
|---|---|---|
| MR | Mantle recession (mantle edge pulled back from the shell lip) | Dehydration, calcium deficiency, bacterial infection, chemical exposure |
| SP | Shell pitting or erosion | Acidic substrate, calcium deficiency, ammonia |
| ST | Thin or cracked shell, chipped lip | Calcium deficiency, handling damage |
| EM | Excess or discoloured mucus | Infection, irritants |
| FO | Foul odour | Bacterial infection, decomposition |
| RF | Retraction failure, unresponsive | Severe illness, dying |
| LE | Lethargy, not feeding | Climate out of range, infection |
| EP | Widespread epiphragm sealing | Climate stress (dry, hot or cold) |
| MI | Visible mites (moving white specks) | *Riccardoella* infestation |
| OT | Other | describe |

**Status rules** (calibrate the baseline per unit):
- **Normal:** daily mortality below 2× the baseline.
- **Alert:** 7-day average at or above 2× the baseline. Review climate, feed, residues and density, and inspect closely.
- **Outbreak:** daily mortality at or above 5× the baseline, or clustered deaths. Isolate the unit and follow SOP M4, section 6.

---

## Log 2: Quarantine and Isolation Register

| Field | Entry |
|---|---|
| Batch / consignment ID | |
| Source (supplier, location; captive-bred or wild) | |
| Arrival date and count | |
| Arrival assessment ref. (SOP M1) | |
| Quarantine room / box | |
| Daily checks (date, dead, signs, initials) | rolling table |
| Earliest release date (arrival + 28–42 days) | `=arrival date + 42` (or 28 minimum) |
| Release decision | Released / extended / rejected and disposed |
| Approved by | |

**Isolation of sick stock** (within existing units): unit ID, date isolated, number isolated, reason (sign codes), outcome (recovered and returned, culled, died), initials.

---

## Log 3: Cleaning and Disinfection Record

| Date | Unit / area | Task (between-batch clean / weekly trough wash / footbath change) | Product and dilution | Contact time | Rinsed? | Dried before restock? | Initials | Verified by |
|---|---|---|---|---|---|---|---|---|
| | | | | | Y / N | Y / N | | |

**Footbath / boot-dip log:** location, date and time changed, product and dilution, initials. Change at least daily, or when visibly soiled.

---

## Log 4: Cold Storage Temperature Log (fridge, chiller and freezer)

| Date | Time | Unit | Target | Reading (°C) | In range? | Corrective action | Product affected / decision | Initials |
|---|---|---|---|---|---|---|---|---|
| | AM | Conditioning chiller (live *Cornu*) | 2–6 °C | | | | | |
| | PM | Conditioning chiller (live *Cornu*) | 2–6 °C | | | | | |
| | AM | *Achatina* conditioning area | 8–12 °C | | | | | |
| | AM | Chilled product fridge | 0–5 °C | | | | | |
| | PM | Chilled product fridge | 0–5 °C | | | | | |
| | AM | Freezer | −18 °C or colder | | | | | |

**Formula for spreadsheet use:** `In range = AND(reading>=min, reading<=max)`, highlighted red if FALSE.

**Thermometer calibration (quarterly):** instrument ID, reference reading, instrument reading, difference, pass (±0.5 °C) or fail, initials.

---

## Log 5: Mortality Disposal Record

| Date | Units | Number / weight disposed | Method (approved animal by-product route, e.g. licensed collector, approved incineration) | Collector / consignment note ref. | Initials |
|---|---|---|---|---|---|

---

## Monthly Review Sign-Off

| Month | Units on Alert | Units in Outbreak | Root causes identified | Corrective actions | Logs complete? | Reviewed by (farm manager) | Date |
|---|---|---|---|---|---|---|---|
