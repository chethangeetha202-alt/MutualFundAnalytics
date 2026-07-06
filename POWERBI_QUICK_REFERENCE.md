# Power BI Dashboard — Quick Reference Card

## Data Import Checklist

### 8 Tables to Import (in order)

| # | Table | File Path | Key Columns | Link To |
|---|-------|-----------|-------------|---------|
| 1 | Scheme Performance | `data/processed/scheme_performance_clean.csv` | amfi_code, scheme_name, category, fund_house, expense_ratio, aum | Main table |
| 2 | NAV History | `data/processed/nav_history_clean.csv` | amfi_code, date, nav | Scheme (amfi_code) |
| 3 | Investor Transactions | `data/processed/investor_transactions_clean.csv` | investor_id, amfi_code, transaction_date, amount, transaction_type, state, age_group, city_tier | Scheme (amfi_code) |
| 4 | Fund Scorecard | `fund_scorecard.csv` | scheme_name, amfi_code, fund_score, cagr_3yr, sharpe_ratio, alpha, beta | Scheme (amfi_code) |
| 5 | Alpha Beta | `alpha_beta.csv` | scheme_name, alpha, beta, tracking_error_nifty100 | Scheme (scheme_name) |
| 6 | Fund Risk Profile | `fund_risk_profile.csv` | scheme_name, amfi_code, risk_grade | Scheme (amfi_code) |
| 7 | AUM by AMC | `data/raw/03_aum_by_fund_house.csv` | fund_house, date, aum | Scheme (fund_house) |
| 8 | Benchmarks | `data/raw/10_benchmark_indices.csv` | date, nifty_50, nifty_100 | Date tables |

---

## KPI Card Templates (Copy These Exactly)

### Card 1: Total AUM
- **Title:** Total AUM
- **Value Field:** Total AUM (measure)
- **Format:** ₹ 81.0 Cr
- **Background Color:** #003DA5 (Bluestock Blue)
- **Text Color:** White

### Card 2: SIP Inflows  
- **Title:** SIP Inflows
- **Value Field:** Total SIP Inflows (measure)
- **Format:** ₹ 31.0K Cr
- **Background Color:** #E3F2FD (Light Blue)
- **Text Color:** Dark

### Card 3: Total Folios
- **Title:** Folios
- **Value Field:** Total Folios (measure)
- **Format:** 26.12 Cr
- **Background Color:** #003DA5 (Bluestock Blue)
- **Text Color:** White

### Card 4: Total Schemes
- **Title:** Schemes
- **Value Field:** Total Schemes (measure)
- **Format:** 1,908
- **Background Color:** #E3F2FD (Light Blue)
- **Text Color:** Dark

---

## Chart Specifications Summary

### PAGE 1 — INDUSTRY OVERVIEW

| Chart | Type | X-Axis | Y-Axis | Size | Location |
|-------|------|--------|--------|------|----------|
| AUM Trend | Line | Date (Monthly) | SUM(AUM) | 50% | Bottom-Left |
| AUM by AMC | Bar | Fund House | SUM(AUM) | 50% | Bottom-Right |

### PAGE 2 — FUND PERFORMANCE

| Chart | Type | X-Axis | Y-Axis | Bubble/Color | Size | Location |
|-------|------|--------|--------|--------------|------|----------|
| Return vs Risk | Scatter | CAGR 3yr | Std Dev | AUM / Category | 60% | Top |
| Fund Scorecard | Table | 10 columns (scheme_name, score, etc.) | - | - | 100% | Middle |
| NAV vs Benchmark | Dual Axis | Date | NAV / NIFTY50 | Line colors | 100% | Bottom |

### PAGE 3 — INVESTOR ANALYTICS

| Chart | Type | Axis | Value | Size | Location |
|-------|------|------|-------|------|----------|
| Transactions by State | Bar | State (Top 10) | SUM(Amount) | 50% | Top-Left |
| Transaction Type | Donut | Categories | SUM(Amount) | 50% | Top-Right |
| Avg by Age Group | Bar | Age Group | AVG(Amount) | 100% | Middle |
| Monthly Volume | Line | Month | COUNT(Investors) | 100% | Bottom |

### PAGE 4 — SIP & MARKET TRENDS

| Chart | Type | Axis | Value | Size | Location |
|-------|------|------|-------|------|----------|
| SIP vs Nifty | Dual Axis Bar+Line | Date | SIP (Bar) / NIFTY50 (Line) | 100% | Top |
| Category Heatmap | Matrix | Category × Month | SUM(Amount) | 100% | Middle |
| Top 5 Categories | Bar | Category (Top 5) | SUM(Amount) FY25 | 100% | Bottom |

---

## Measure Formulas (Copy-Paste Ready)

### Profit & Loss Measures
```dax
Total AUM = SUMX(Scheme Performance, [AUM]) / 10000000
Total SIP Inflows = SUMX(FILTER(Investor Transactions, [transaction_type] = "SIP"), [amount]) / 10000000
```

### Count Measures
```dax
Total Folios = DISTINCTCOUNT(Investor Transactions[investor_id])
Total Schemes = DISTINCTCOUNT(Scheme Performance[scheme_name])
Total Investors = DISTINCTCOUNT(Investor Transactions[investor_id])
```

### Average Measures
```dax
Avg Sharpe = AVERAGE(Fund Scorecard[sharpe_ratio])
Avg Fund Score = AVERAGE(Fund Scorecard[fund_score])
Avg Portfolio = AVERAGE(Investor Transactions[amount])
Avg Alpha = AVERAGE(Alpha Beta[alpha])
Avg Beta = AVERAGE(Alpha Beta[beta])
```

### Category Measures
```dax
Category AUM = SUMX(FILTER(Scheme Performance, [category] = SELECTEDVALUE(Scheme Performance[category])), [AUM])
SIP by Category = SUMX(FILTER(Investor Transactions, [transaction_type] = "SIP" && [category] = SELECTEDVALUE(Scheme Performance[category])), [amount])
```

---

## Color Palette (Hex Codes)

| Use | Color Name | Hex Code |
|-----|-----------|----------|
| Primary | Bluestock Blue | #003DA5 |
| Secondary | Light Blue | #E3F2FD |
| Positive | Green | #4CAF50 |
| Alert | Orange | #FF9800 |
| Negative | Red | #F44336 |
| Neutral | Gray | #424242 |
| Background | White | #FFFFFF |

---

## Slicer Configuration (All Pages)

### Page 2 — Fund Performance Slicers
1. **Fund House** — Scheme Performance[fund_house] (Dropdown)
2. **Category** — Scheme Performance[category] (Dropdown)
3. **Plan Type** — Scheme Performance[plan_type] (Dropdown)

### Page 3 — Investor Analytics Slicers
1. **State** — Investor Transactions[state] (Dropdown)
2. **Age Group** — Investor Transactions[age_group] (Dropdown)
3. **City Tier** — Investor Transactions[city_tier] (Dropdown)

### Slicer Settings
- **Type:** Dropdown (Vertical list also works)
- **Multiple Selection:** ON
- **Show "Select All":** ON
- **Sort:** A-Z

---

## Drill-Through Setup (Page 2 → NAV Detail)

**Source Page:** Fund Performance (Fund Scorecard table)  
**Target Page:** NAV Detail (new page)  
**Drill-Through Field:** Scheme Name

**NAV Detail Page Content:**
1. **Page Title:** "{Scheme Name} NAV Trend" (dynamic)
2. **Line Chart:** 
   - X-Axis: NAV History[date]
   - Y-Axis: NAV History[nav]
   - Filtered by selected Scheme Name
3. **KPI Card:** Current NAV value
4. **Back Button:** Enable drill-back

---

## Conditional Formatting Guide

### Fund Scorecard Table — Fund Score Column
```
Condition 1: If value >= 80 → Green (#4CAF50)
Condition 2: If value >= 60 → Yellow (#FFC107)
Condition 3: If value < 60 → Red (#F44336)
```

### Heatmap — Category Inflow
```
Color Scale:
  Minimum: Light Red (#FFEBEE)
  Center: White (#FFFFFF)
  Maximum: Dark Green (#2E7D32)
```

---

## Export Settings

### PDF Export
- **Orientation:** Landscape
- **Include all pages:** Yes
- **Resolution:** Default
- **Margins:** Standard

### PNG Export (Each Page)
- **Format:** PNG
- **Quality:** Maximum (300 DPI)
- **Resolution:** 1920×1080 minimum
- **Naming:** Page[#]_[PageTitle].png

---

## Data Types to Verify

| Table | Column | Type | Format |
|-------|--------|------|--------|
| Scheme Performance | aum | Whole Number | Currency |
| Scheme Performance | expense_ratio | Decimal | Percentage |
| NAV History | nav | Decimal | Currency |
| NAV History | date | Date | Date |
| Investor Transactions | amount | Whole Number | Currency |
| Investor Transactions | transaction_date | Date | Date |
| Fund Scorecard | fund_score | Decimal | Number (0-100) |
| Fund Scorecard | cagr_3yr | Decimal | Percentage |

**To Change Data Type in Power BI:**
1. Go to Data view
2. Select column header
3. Column Tools > Data Type (dropdown)
4. Select appropriate type

---

## Common Mistakes to Avoid

❌ **Forgetting to create relationships** → Charts will show blanks  
✅ **Solution:** Model view → drag columns to create links

❌ **Using SUM instead of AVERAGE** → KPI shows wrong values  
✅ **Solution:** Use correct aggregation function

❌ **Date format issues** → Timeline slicer won't work  
✅ **Solution:** Ensure Date columns are Date type, not Text

❌ **Slicers not syncing** → Different charts show different data  
✅ **Solution:** Edit interactions → set all to "Filter"

❌ **Too many rows in table** → Performance slow  
✅ **Solution:** Filter to Top N or create aggregated view

---

## Testing Checklist

- [ ] All 4 pages created
- [ ] All KPI cards show correct values
- [ ] All charts render with data (no blanks)
- [ ] Slicers work and filter charts
- [ ] Drill-through from table to NAV page works
- [ ] Tooltips display on hover
- [ ] Export to PDF produces 4-page document
- [ ] Export each page as PNG at 300 DPI
- [ ] Colors match Bluestock branding
- [ ] Logo visible on all pages
- [ ] Data is current (latest NAV date shown)

---

## Quick Fixes (If Something Breaks)

**Problem:** "This visualization can't be loaded"
- **Fix:** Remove filter, re-add field, check relationships

**Problem:** "Some fields aren't recognized"
- **Fix:** Reload data, refresh tables, check column names

**Problem:** Chart shows "No data available"
- **Fix:** Verify relationship exists, remove filter context, check Data view

**Problem:** Export fails
- **Fix:** Save file first, close other Power BI windows, try again

---

## Completion Verification

### Save as .pbix
```
File > Save As
Filename: bluestock_mf_dashboard.pbix
Location: C:\Users\cheth\Downloads\MutualFundAnalytics\
```

### Export to PDF
```
File > Export > Export to PDF
Filename: Dashboard.pdf
Include all pages: YES
```

### Export Pages as PNG
```
For each page:
  File > Export > Export image
  Format: PNG
  Filename: Page[#]_[Title].png
```

### Final Deliverables
```
✓ bluestock_mf_dashboard.pbix (1 file)
✓ Dashboard.pdf (all 4 pages)
✓ Page1_Industry_Overview.png
✓ Page2_Fund_Performance.png
✓ Page3_Investor_Analytics.png
✓ Page4_SIP_Market_Trends.png
```

---

**Ready to Start?** Open Power BI Desktop and follow the POWERBI_IMPLEMENTATION_GUIDE.md step-by-step! 🚀
