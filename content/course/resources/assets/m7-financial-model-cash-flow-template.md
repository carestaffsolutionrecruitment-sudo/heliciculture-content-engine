# Module 7 Downloadable: Financial Model and Cash Flow Template

**Commercial Heliculture Masterclass · Snail World (snailworld.org)**
**Format:** spreadsheet with 8 tabs. Input cells are yellow, formula cells grey and locked, and key outputs sit on the Dashboard. The model contains **no pre-filled prices**: enter local quotes and confirmed buyer prices, because borrowed figures make the model misleading.

---

## Tab 1: Assumptions

| Section | Field | Unit |
|---|---|---|
| **Farm** | Species; production system; productive area | text; text; m² |
| **Production** | Stocking density (grower stage) | snails/m² |
| | Survival rate, hatch to harvest | % |
| | Cycle length, hatch to harvest | months |
| | Cycles per year (per area) | = 12 ÷ cycle length (rounded down if not continuous) |
| | Average harvest live weight | g |
| | Meat yield (clean meat ÷ live weight) | % |
| | Breeders held; hatchlings per breeder per year | number |
| **Feed** | Feed conversion ratio (meal kg ÷ live weight gain kg) | ratio |
| | Feed cost per kg (from the Module 3 calculator) | currency/kg |
| **Labour** | Hours per week (husbandry, processing, admin); hourly cost | h; currency/h |
| **Energy** | Heating, cooling, misting, cold storage kWh per month; tariff | kWh; currency/kWh |
| **Prices** (by channel) | Live snails per kg; clean meat per kg; prepared product per unit; caviar per jar; mucin per litre; shell grit per kg | currency |
| **Sales mix** | % of output sold live / clean meat / prepared | % (must total 100) |
| **By-products** | Caviar jars per cycle; mucin litres per cycle; shell kg per cycle | number |
| **Finance** | Opening cash; loan amount, interest rate, term; grant income | currency; %; months |
| **Tax** | Tax rate on profit (simplified) | % |
| **Inflation** | Annual cost inflation; annual price change | % |

---

## Tab 2: Capital Expenditure (CapEx)

| Category | Item | Qty | Unit cost | Total (`=Qty*Unit cost`) | Useful life (yrs) | Annual depreciation (`=Total/Life`) | Purchase month |
|---|---|---|---|---|---|---|---|
| Land and site | Land purchase or lease premium; clearing; levelling; drainage | | | | | | |
| Pens and buildings | Pens, trenches, hutches, polytunnel or building, racking, boxes, lids | | | | | | |
| Escape and predator control | Perimeter netting, anti-escape wire and energiser, mesh, rodent control | | | | | | |
| Climate control | Misting system, humidistat, heaters, coolers, fans, data loggers, alarms, back-up power | | | | | | |
| Water | Tanks, pump (e.g. solar borehole), pipework, filters | | | | | | |
| Scales and equipment | Weighing scales (precision and platform), pH meter, thermometers, tools | | | | | | |
| Processing | Boilers, stainless tables, chiller, freezer, vacuum packer, sinks | | | | | | |
| Initial stock | Breeders or juveniles, quarantine setup | | | | | | |
| Pre-operating | Registration, permits, legal, training, initial testing | | | | | | |
| **Total CapEx** | | | | `=SUM(...)` | | `=SUM(...)` | |

---

## Tab 3: Operating Expenses (OpEx), Monthly

| Category | Line items | Formula basis |
|---|---|---|
| Feed | Meal; fresh forage; calcium supplements | live weight gain × FCR × feed cost, from the production schedule |
| Utilities | Electricity, fuel, water | kWh × tariff; metered water |
| Labour | Wages and on-costs | hours × hourly cost × 4.33 |
| Substrate and consumables | Substrate, disinfectant, gloves, footbath product | monthly estimate |
| Packaging | Trays, vacuum bags, jars, labels, insulated boxes, ice packs | units sold × cost per unit |
| Transport and distribution | Deliveries, courier | per delivery × deliveries |
| Compliance and testing | Lab tests, registration fees, audits | schedule |
| Veterinary and advice | Visits, diagnostics | schedule |
| Insurance | Liability, stock, buildings | annual ÷ 12 |
| Marketing | Website, listings, samples, events | monthly budget |
| Repairs and maintenance | % of CapEx per year ÷ 12 | assumption |
| Finance costs | Loan interest | from the loan schedule |
| **Total OpEx** | | `=SUM(...)` |

---

## Tab 4: Production Schedule (monthly, 36 months)

| Row | Formula |
|---|---|
| Snails stocked (by batch and month) | input schedule |
| Snails surviving to harvest | `=stocked × survival rate` |
| Harvest month | `=stocking month + cycle length` |
| Live weight harvested (kg) | `=surviving × harvest weight g ÷ 1000` |
| Clean meat (kg) | `=live weight × meat yield %` |
| Caviar jars, mucin litres, shell kg | from the assumptions, per cycle |

---

## Tab 5: Revenue Projections (monthly)

| Stream | Formula |
|---|---|
| Live snail sales | `=live kg × % sold live × live price per kg` |
| Clean meat sales | `=clean meat kg × % sold as meat × meat price per kg` |
| Prepared products | `=units × unit price` |
| Caviar | `=jars × price per jar` |
| Mucin | `=litres × price per litre` |
| Shells | `=kg × price per kg` |
| **Total revenue** | `=SUM(...)` |

---

## Tab 6: Profit and Break-Even

| Measure | Formula |
|---|---|
| Gross margin | `=revenue − variable costs (feed, packaging, transport, consumables)` |
| Gross margin per m² per year | `=annual gross margin ÷ productive area` |
| EBITDA | `=gross margin − fixed operating costs` |
| Net profit before tax | `=EBITDA − depreciation − interest` |
| **Break-even price per kg (clean meat equivalent)** | `=(annual fixed costs + annual variable costs) ÷ annual saleable kg` |
| **Break-even volume (kg per year)** | `=annual fixed costs ÷ (price per kg − variable cost per kg)` |
| **Simple payback (years)** | `=total CapEx ÷ average annual net cash flow` |
| **Return on investment (%)** | `=average annual net profit ÷ total CapEx × 100` |

---

## Tab 7: Cash Flow Forecast (36 months)

| Row | Month 1 … Month 36 |
|---|---|
| Opening cash balance | = previous month's closing balance (Month 1 = opening cash) |
| **Receipts:** sales receipts (with a payment-terms lag, e.g. +30 days for B2B), loan drawdown, grants, owner investment | |
| **Payments:** CapEx purchases (by purchase month), OpEx (Tab 3), loan repayments, tax | |
| Net cash flow | `=total receipts − total payments` |
| Closing cash balance | `=opening + net cash flow` |
| Cash warning | `=IF(closing<0,"SHORTFALL","")` (red) |
| Cumulative cash position | running total |

**Annual summaries:** Year 1, Year 2 and Year 3 totals for receipts, payments, net cash flow and closing balance.

---

## Tab 8: Sensitivity and Dashboard

**Sensitivity table:** net profit (Year 2) and payback under each change:

| Scenario | Change |
|---|---|
| Survival | −10 points / −20 points |
| Cycle length | +1 month / +2 months |
| Price | −15 % / −25 % |
| Feed cost | +20 % |
| Energy cost | +30 % |

**Dashboard:** total CapEx; months to cash breakeven; lowest cash balance and the month it occurs; Year 1–3 revenue and net profit; gross margin per m²; break-even price against the planned average price; payback; ROI.

> **Model conservatively:** assume higher mortality and a longer cycle in Year 1, and include a learning curve of one to two cycles.
