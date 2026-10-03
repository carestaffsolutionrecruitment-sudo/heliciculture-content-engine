# Module 3 Downloadable: Weekly Feed Formulation and Stocking Density Calculator

**Commercial Heliculture Masterclass · Snail World (snailworld.org)**
**Format:** spreadsheet (Excel or Google Sheets) with 5 tabs. Input cells are shaded yellow, formula cells grey and locked, and warning cells use conditional formatting (red for a fail, amber for a warning).

> All targets are indicative starting points from published husbandry literature and producer practice. Calibrate them with laboratory feed analysis and your own growth records.

---

## Tab 1: Settings and Targets

| Cell | Field | Default | Notes |
|---|---|---|---|
| B2 | Species | *Cornu aspersum* / *Achatina* group (dropdown) | Drives the targets below |
| B3 | Limestone calcium content (%) | 38 | Use the supplier's certificate; typically 36–40 % |
| B4 | Oyster shell calcium content (%) | 36 | Typically 35–38 % |
| B5 | Meal dry matter (%) | 90 | Typical for dry mixed meal |

**Nutrient and density targets** (looked up from B2):

| Stage | *Cornu* crude protein (DM) | *Cornu* calcium (DM) | *Achatina* crude protein (DM) | *Achatina* calcium (DM) | *Cornu* max density (/m²) | *Achatina* max density (/m²) | Starting feed rate (% live weight per day, as meal) |
|---|---|---|---|---|---|---|---|
| Hatchling / nursery | 18–20 % | 10–12 % | 20–24 % | 8–10 % | 1,500–2,000 | 100 | 5–8 % |
| Grower / fattening | 15–18 % | 10–13 % | 18–22 % | 8–12 % | 300–500 | 20–50 | 3–5 % |
| Breeder | 16–18 % | 12–14 % | 18–20 % | 10–12 % | 100–150 | 5–10 | 2–4 % |

**Salt (NaCl) target for every stage: 0 %.** Any salt in a formula triggers a red FAIL.

---

## Tab 2: Feed Formulation

**Input table (rows 6–20):**

| Col | Field | Example |
|---|---|---|
| A | Ingredient | Ground maize |
| B | Inclusion (kg per 100 kg) | 28 |
| C | Dry matter (%) | 88 |
| D | Crude protein (% as fed) | 9 |
| E | Calcium (% as fed) | 0.02 |
| F | Phosphorus (% as fed) | 0.28 |
| G | Contains salt? (Y/N) | N |
| H | Price per kg | (local) |

**Formulas (row 22, totals):**

| Output | Formula |
|---|---|
| Total inclusion | `=SUM(B6:B20)` → must equal 100 (red if not) |
| Crude protein, as fed (%) | `=SUMPRODUCT(B6:B20,D6:D20)/SUM(B6:B20)` |
| Calcium, as fed (%) | `=SUMPRODUCT(B6:B20,E6:E20)/SUM(B6:B20)` |
| Phosphorus, as fed (%) | `=SUMPRODUCT(B6:B20,F6:F20)/SUM(B6:B20)` |
| Formula dry matter (%) | `=SUMPRODUCT(B6:B20,C6:C20)/SUM(B6:B20)` |
| Crude protein, DM basis (%) | `= CP as fed ÷ (formula DM ÷ 100)` |
| Calcium, DM basis (%) | `= Ca as fed ÷ (formula DM ÷ 100)` |
| Ca:P ratio | `= Ca ÷ P` |
| Cost per kg of feed | `=SUMPRODUCT(B6:B20,H6:H20)/SUM(B6:B20)` |
| Salt check | `=IF(COUNTIF(G6:G20,"Y")>0,"FAIL – remove salt","OK")` |
| Protein check | Compare the DM value with the Tab 1 target for the stage: below target = amber, above target +3 = amber, in range = green |
| Calcium check | As for protein |

### Dry matter vs moisture

Snails eat both dry meal and wet forage, so compare nutrients on a **dry-matter (DM)** basis:

- **Nutrient % (DM)** = nutrient % (as fed) ÷ (DM % ÷ 100)
- **Moisture %** = 100 − DM %
- **Dry matter supplied (g)** = fresh weight (g) × DM % ÷ 100

Example: fresh chard at 8 % DM and 2 % crude protein (as fed) is 2 ÷ 0.08 = **25 % crude protein on a DM basis**. But 100 g of it supplies only 8 g of dry matter.

**Combined ration (meal plus forage), DM basis:**

- Ration CP % (DM) = (meal DM g × meal CP % DM + forage DM g × forage CP % DM) ÷ (meal DM g + forage DM g)

The same formula applies to calcium.

### Calcium carbonate supplementation

To raise a base mix to a target calcium level using limestone, accounting for the dilution limestone causes:

**Limestone (g per kg of finished feed) = 1,000 × (T − B) ÷ (L − B)**

where T = target calcium %, B = calcium % of the base mix without limestone, and L = calcium % of the limestone (Tab 1, B3).

> **Worked example:** base mix B = 1.0 % Ca, target T = 12 % Ca, limestone L = 40 % Ca.
> Limestone = 1,000 × (12 − 1) ÷ (40 − 1) = **282 g per kg of feed** (about 28 kg per 100 kg). This matches the *Cornu* grower formula in Module 3.

Spreadsheet formula: `=1000*(T-B)/(L-B)`, with a check that `L > T > B`.

---

## Tab 3: Weekly Feed Requirement

| Col | Field | Formula / input |
|---|---|---|
| A | Unit / pen ID | input |
| B | Stage | dropdown |
| C | Number of snails | input (from the latest count) |
| D | Average live weight (g) | input (from the fortnightly sample) |
| E | Feed rate (% live weight per day) | default from Tab 1 for the stage; editable |
| F | Batch live weight (kg) | `=C*D/1000` |
| G | Daily meal (kg) | `=F*E/100` |
| H | Weekly meal (kg) | `=G*7` |
| I | Weekly feed cost | `=H*Tab2!CostPerKg` |
| J | Previous-morning residue | dropdown: none / small / large |
| K | Adjusted daily meal (kg) | `=IF(J="none",G*1.1,IF(J="large",G*0.9,G))` |

**Totals:** total weekly meal (kg), total weekly cost, and the meal to mix this week, rounded up to the nearest 5 kg.

---

## Tab 4: Stocking Density

| Col | Field | Formula / input |
|---|---|---|
| A | Unit / pen ID | input |
| B | Stage | dropdown |
| C | Usable surface area (m²) | input (floor + walls + shelters + tray sides in contact with snails) |
| D | Current number | input |
| E | Current density (/m²) | `=D/C` |
| F | Maximum density (/m²) | lookup from Tab 1 (upper value for stage and species) |
| G | Maximum stock | `=ROUNDDOWN(C*F,0)` |
| H | Surplus to move | `=MAX(0,D-G)` |
| I | Status | `=IF(E>F,"OVER – grade/split","OK")` (red if over) |

---

## Tab 5: Growth and Feed Conversion Tracker

| Col | Field | Formula / input |
|---|---|---|
| A | Batch ID | input |
| B | Sample date | input (every 14 days) |
| C | Sample size (n) | input (30–50) |
| D | Mean live weight (g) | input |
| E | Live count | input |
| F | Batch live weight (kg) | `=D*E/1000` |
| G | Meal fed since last sample (kg) | sum from Tab 3 history |
| H | Weight gain since last sample (kg) | `=F - F(previous)` |
| I | Feed conversion ratio | `=IF(H>0,G/H,"no gain – investigate")` |
| J | Days to target weight (projection) | `=(target g − D) ÷ daily gain g` |

A chart plots mean live weight (D) against date for each batch.
