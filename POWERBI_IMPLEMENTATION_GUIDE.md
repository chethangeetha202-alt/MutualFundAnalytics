# Power BI Dashboard Implementation Guide
## Bluestock Mutual Fund Analytics Dashboard

**Completion Time:** 15-20 minutes in Power BI Desktop  
**Data Source:** Cleaned CSVs + cleaned NAV history  
**Output:** bluestock_mf_dashboard.pbix + 4 page PNGs

---

## SECTION 1: DATA IMPORT & SETUP (5 minutes)

### Step 1.1: Create New Power BI Desktop File
1. Open **Power BI Desktop**
2. Click **File > New**
3. Save as: `bluestock_mf_dashboard.pbix` in root directory

### Step 1.2: Import CSV Files
**Import these 8 tables:**

1. **Scheme Performance** (`data/processed/scheme_performance_clean.csv`)
   - Columns: amfi_code, scheme_name, category, expense_ratio, aum, ...
   - Set as main table

2. **NAV History** (`data/processed/nav_history_clean.csv`)
   - Columns: amfi_code, date, nav
   - Link on amfi_code

3. **Investor Transactions** (`data/processed/investor_transactions_clean.csv`)
   - Columns: investor_id, amfi_code, transaction_date, amount, transaction_type, state, age_group, ...

4. **Fund Scorecard** (`fund_scorecard.csv`)
   - Columns: scheme_name, amfi_code, fund_score, cagr_3yr, sharpe_ratio, alpha, beta, ...

5. **Alpha Beta** (`alpha_beta.csv`)
   - Columns: scheme_name, alpha, beta, tracking_error_nifty100

6. **Fund Risk Profile** (`fund_risk_profile.csv`)
   - Columns: scheme_name, amfi_code, risk_grade, ...

7. **AUM by Fund House** (`data/raw/03_aum_by_fund_house.csv`)
   - Columns: fund_house, date, aum

8. **Benchmark Indices** (`data/raw/10_benchmark_indices.csv`)
   - Columns: date, nifty_50, nifty_100

**Import Steps:**
- Home > Get Data > Text/CSV
- Select file > Load
- Repeat for all 8 tables

### Step 1.3: Create Relationships
Navigate to **Model** view and create these relationships:

| From Table | Column | To Table | Column |
|-----------|--------|----------|--------|
| Scheme Performance | amfi_code | NAV History | amfi_code |
| Scheme Performance | amfi_code | Investor Transactions | amfi_code |
| Scheme Performance | amfi_code | Fund Scorecard | amfi_code |
| Scheme Performance | scheme_name | Alpha Beta | scheme_name |
| Scheme Performance | scheme_name | Fund Risk Profile | scheme_name |
| AUM by Fund House | fund_house | Scheme Performance | fund_house |
| NAV History | date | Benchmark Indices | date |

**Relationship Settings:**
- **Cardinality:** Many-to-One (Many sides → scheme_performance)
- **Cross filter:** Both
- **Active:** Yes

### Step 1.4: Create Date Table (Optional but Recommended)
In **Data** view, add a new table:

```
Date = CALENDAR(DATE(2022,1,1), TODAY())
```

Then create columns:
```
Year = YEAR([Date])
Month = MONTH([Date])
Quarter = QUARTER([Date])
MonthYear = FORMAT([Date], "MMM-YYYY")
```

---

## SECTION 2: KPI METRICS & CALCULATED COLUMNS (3 minutes)

### Create These Measures in Scheme Performance Table

**In Power BI:** Table name > New Measure > Paste formula

#### 2.1: Total AUM (₹ Crores)
```dax
Total AUM = SUMX(Scheme Performance, [AUM]) / 10000000
```

#### 2.2: Total SIP Inflows (₹ Crores)
```dax
Total SIP Inflows = SUMX(
    FILTER(Investor Transactions, [transaction_type] = "SIP"),
    [amount]
) / 10000000
```

#### 2.3: Total Folios
```dax
Total Folios = DISTINCTCOUNT(Investor Transactions[investor_id])
```

#### 2.4: Total Schemes
```dax
Total Schemes = DISTINCTCOUNT(Scheme Performance[scheme_name])
```

#### 2.5: Average Sharpe Ratio
```dax
Avg Sharpe = AVERAGE(Fund Scorecard[sharpe_ratio])
```

#### 2.6: Average Fund Score
```dax
Avg Fund Score = AVERAGE(Fund Scorecard[fund_score])
```

#### 2.7: Total AUM by Category
```dax
Category AUM = SUMX(
    FILTER(Scheme Performance, Scheme Performance[category] = SELECTEDVALUE(Scheme Performance[category])),
    [AUM]
)
```

#### 2.8: SIP Count by Type
```dax
SIP Count = COUNTX(
    FILTER(Investor Transactions, [transaction_type] = "SIP"),
    Investor Transactions[investor_id]
)
```

---

## SECTION 3: PAGE 1 — INDUSTRY OVERVIEW (4 minutes)

### Page Title: "Industry Overview"

### 3.1: KPI Cards (Top Section)
Create 4 card visuals in a row:

**Card 1: Total AUM**
- Value field: Total AUM measure
- Format: ₹ 81.0 Cr
- Background: Bluestock Blue (#003DA5)
- Text: White

**Card 2: SIP Inflows**
- Value field: Total SIP Inflows measure
- Format: ₹ 31.0K Cr
- Background: Light Blue (#E3F2FD)
- Text: Dark

**Card 3: Total Folios**
- Value field: Total Folios measure
- Format: 26.12 Cr
- Background: Bluestock Blue (#003DA5)
- Text: White

**Card 4: Total Schemes**
- Value field: Total Schemes measure
- Format: 1,908
- Background: Light Blue (#E3F2FD)
- Text: Dark

### 3.2: Line Chart — Industry AUM Trend (2022-2025)
**Position:** Below KPI cards, left 50%

- **X-axis:** AUM by Fund House[date] (Month/Year)
- **Y-axis:** SUM(AUM by Fund House[aum])
- **Legend:** AUM by Fund House[fund_house]
- **Lines:** One per fund house
- **Data Labels:** Off
- **Grid Lines:** On (Y-axis only)
- **Title:** "Industry AUM Trend (2022-2025)"
- **Format:** Currency, 0 decimals

### 3.3: Bar Chart — AUM by AMC (Top 15)
**Position:** Below KPI cards, right 50%

- **Category (X-axis):** Scheme Performance[fund_house]
- **Value (Y-axis):** SUM(Scheme Performance[aum])
- **Sort by value:** Descending
- **Show top:** 15 funds
- **Data Labels:** On (Value)
- **Title:** "Top 15 AMCs by AUM"
- **Color:** Bluestock gradient

---

## SECTION 4: PAGE 2 — FUND PERFORMANCE (5 minutes)

### Page Title: "Fund Performance"

### 4.1: Scatter Plot — Return vs Risk
**Position:** Top section

- **X-axis:** Fund Scorecard[cagr_3yr] (3yr CAGR)
- **Y-axis:** NAV History (Std Dev of returns)
- **Bubble size:** Scheme Performance[aum]
- **Legend/Category:** Scheme Performance[category]
- **Title:** "Fund Return vs Risk (Bubble = AUM)"
- **X Title:** "3-Year CAGR (%)"
- **Y Title:** "Risk (Std Dev)"
- **Data Labels:** Scheme Performance[scheme_name] (on hover)

### 4.2: Fund Scorecard Table
**Position:** Middle section, full width

**Columns (in order):**
1. Scheme Name
2. Category
3. Fund Score (0-100)
4. 3yr CAGR (%)
5. Sharpe Ratio
6. Alpha
7. Beta
8. Expense Ratio (%)
9. AUM (₹ Cr)
10. Risk Grade

**Configuration:**
- **Sort by:** Fund Score (Descending)
- **Conditional formatting:** Fund Score column
  - Green: 80-100
  - Yellow: 60-80
  - Red: < 60
- **Alternating row colors:** Enable
- **Show rows:** 50 (paginated)

### 4.3: Line Chart — NAV vs Benchmark
**Position:** Bottom section

- **X-axis:** NAV History[date]
- **Y-axis (Primary):** NAV History[nav] (normalized to 100)
- **Y-axis (Secondary):** Benchmark Indices[nifty_50] (normalized to 100)
- **Title:** "Fund NAV vs NIFTY 50 Benchmark"
- **Data Labels:** Off
- **Legend:** Top right

### 4.4: Slicers (Right Panel)
Add 3 dropdown slicers:

**Slicer 1: Fund House**
- Field: Scheme Performance[fund_house]
- Type: List
- Position: Right, top
- Style: Dropdown

**Slicer 2: Category**
- Field: Scheme Performance[category]
- Type: List
- Position: Right, middle
- Style: Dropdown

**Slicer 3: Plan Type**
- Field: Scheme Performance[plan_type]
- Type: List
- Position: Right, bottom
- Style: Dropdown

---

## SECTION 5: PAGE 3 — INVESTOR ANALYTICS (5 minutes)

### Page Title: "Investor Analytics"

### 5.1: Bar Chart — Transactions by State
**Position:** Top-left

- **Category (X-axis):** Investor Transactions[state]
- **Value (Y-axis):** SUM(Investor Transactions[amount])
- **Sort by value:** Descending
- **Show top:** 10 states
- **Data Labels:** On (Value)
- **Title:** "Top 10 States by Transaction Amount"
- **Color:** Bluestock Blue

### 5.2: Donut Chart — Transaction Type Split
**Position:** Top-right

- **Legend:** Investor Transactions[transaction_type]
- **Values:** SUM(Investor Transactions[amount])
- **Categories:** SIP / Lumpsum / Redemption
- **Data Labels:** On (Category + %)
- **Title:** "Transaction Type Distribution"
- **Colors:**
  - SIP: Green (#4CAF50)
  - Lumpsum: Blue (#2196F3)
  - Redemption: Orange (#FF9800)

### 5.3: Bar Chart — Age Group vs Avg SIP
**Position:** Middle-full width

- **Category (X-axis):** Investor Transactions[age_group]
- **Value (Y-axis):** AVERAGE(Investor Transactions[amount])
- **Title:** "Average SIP Amount by Age Group"
- **Data Labels:** On (Value)
- **Color:** Gradient (Blue → Light Blue)

### 5.4: Line Chart — Monthly Transaction Volume
**Position:** Bottom-full width

- **X-axis:** Investor Transactions[transaction_date] (Month)
- **Y-axis:** COUNT(Investor Transactions[investor_id])
- **Title:** "Monthly Unique Investors"
- **Data Labels:** Off
- **Grid Lines:** On (Y-axis)

### 5.5: Slicers (Right Panel)
Add 3 dropdown slicers:

**Slicer 1: State**
- Field: Investor Transactions[state]
- Type: List

**Slicer 2: Age Group**
- Field: Investor Transactions[age_group]
- Type: List

**Slicer 3: City Tier**
- Field: Investor Transactions[city_tier]
- Type: List

---

## SECTION 6: PAGE 4 — SIP & MARKET TRENDS (5 minutes)

### Page Title: "SIP & Market Trends"

### 6.1: Dual-Axis Chart — SIP Inflow vs Nifty 50
**Position:** Top section, full width

- **Primary Y-axis (Bar):** Monthly SIP Inflows (₹ Cr)
  - Data: SUMX(FILTER(Investor Transactions, type="SIP"), amount)
  - Color: Blue (#2196F3)
  
- **Secondary Y-axis (Line):** Nifty 50 Index
  - Data: Benchmark Indices[nifty_50]
  - Color: Orange (#FF9800)
  
- **X-axis:** Date (Month/Year)
- **Period:** 2022-2025
- **Title:** "SIP Inflows vs Nifty 50 (Dual Axis)"
- **Data Labels:** Off

### 6.2: Category Inflow Heatmap
**Position:** Middle section

**Setup as Matrix:**
- **Rows:** Scheme Performance[category]
- **Columns:** Date[MonthYear]
- **Values:** SUM(Investor Transactions[amount]) / 10000000
- **Conditional Formatting:** Color scale
  - Minimum (Low): Light red
  - Center: White
  - Maximum (High): Dark green
- **Title:** "Category Inflow Heatmap (₹ Cr)"

### 6.3: Bar Chart — Top 5 Categories by Net Inflow FY25
**Position:** Bottom section

- **Category (X-axis):** Scheme Performance[category]
- **Value (Y-axis):** SUM(Investor Transactions[amount]) filtered to FY25
- **Sort by value:** Descending
- **Show top:** 5
- **Data Labels:** On (Value)
- **Title:** "Top 5 Categories by Net Inflow (FY25)"
- **Color:** Bluestock gradient

---

## SECTION 7: BRANDING & DESIGN (2 minutes)

### 7.1: Color Theme
**Apply Bluestock Color Palette:**

| Element | Color | Hex |
|---------|-------|-----|
| Primary Blue | Bluestock Blue | #003DA5 |
| Light Blue | Background | #E3F2FD |
| Accent 1 | Green | #4CAF50 |
| Accent 2 | Orange | #FF9800 |
| Accent 3 | Red | #F44336 |
| Neutral | Dark Gray | #424242 |
| Background | White | #FFFFFF |

**Apply to Power BI:**
1. View > Themes > Upload custom theme (if available)
2. Alternatively: Select each visual > Format > Colors
3. Use hex codes above

### 7.2: Logo & Branding
1. **Add Logo to Each Page:**
   - Insert > Image
   - Choose Bluestock logo from `dashboard/pbix_assets/`
   - Position: Top-left corner
   - Size: 40x40 pixels
   - Transparency: 80%

2. **Page Headers:**
   - Add text box with page title
   - Font: Segoe UI / Font size: 24 / Bold
   - Color: Bluestock Blue

3. **Footer:**
   - Add text box at bottom
   - Text: "Bluestock Mutual Fund Analytics | Dashboard v1.0"
   - Font size: 10 / Color: Gray

### 7.3: Formatting Standards
- **Currency format:** ₹ (Indian Rupee)
- **Number decimals:** 2 (except percentages: 1 decimal)
- **Font family:** Segoe UI (default)
- **Font size:** 11pt (body), 14pt (titles)
- **Alignment:** Left (text), Right (numbers)

---

## SECTION 8: INTERACTIVITY & TOOLTIPS (2 minutes)

### 8.1: Drill-Through from Fund Table to NAV Detail
1. **Create new page:** Page > New page
2. **Name it:** "NAV Detail"
3. **Add drill-through field:** Fund Scorecard[scheme_name]
4. **Create NAV line chart on this page:**
   - X-axis: NAV History[date]
   - Y-axis: NAV History[nav]
   - Filtered by selected scheme_name
5. **Go back to Page 2 (Fund Performance):**
   - Right-click Fund Scorecard table
   - Drill-through enabled on scheme_name

### 8.2: Custom Tooltips
**For Scatter Plot (Page 2):**
1. Right-click Scatter visual > Format visual
2. Tooltip page: Create basic tooltip showing:
   - Scheme Name
   - 3yr CAGR
   - Risk (Std Dev)
   - AUM
   - Fund Score

**For Line Charts:**
- Show: Date, Value, Series name
- Format: Default (auto)

### 8.3: Slicer Sync
**All pages' slicers should sync:**
- Edit interactions: Select all charts
- Slicer > Interaction: Apply to all
- Cross-filter: Both directions

---

## SECTION 9: EXPORT & FINAL DELIVERY (3 minutes)

### 9.1: Save Power BI File
1. File > Save
2. Save as: `bluestock_mf_dashboard.pbix`
3. Location: Root directory

### 9.2: Export to PDF
1. File > Export > Export to PDF
2. Include all 4 pages
3. Landscape orientation
4. Save as: `Dashboard.pdf`

### 9.3: Export Each Page as PNG
For each of the 4 pages:

1. Navigate to page
2. File > Export > Export image
3. Format: PNG
4. Quality: Maximum (300 DPI)
5. Save as:
   - `Page1_Industry_Overview.png`
   - `Page2_Fund_Performance.png`
   - `Page3_Investor_Analytics.png`
   - `Page4_SIP_Market_Trends.png`

### 9.4: Verify Deliverables
Final file list in root directory:
```
✓ bluestock_mf_dashboard.pbix          (Main file)
✓ Dashboard.pdf                        (All pages)
✓ Page1_Industry_Overview.png          (High-res)
✓ Page2_Fund_Performance.png           (High-res)
✓ Page3_Investor_Analytics.png         (High-res)
✓ Page4_SIP_Market_Trends.png          (High-res)
```

---

## QUICK REFERENCE: DAX FORMULAS

### Copy-Paste Ready Measures

```dax
Total AUM = SUMX(Scheme Performance, [AUM]) / 10000000

Total SIP Inflows = SUMX(FILTER(Investor Transactions, [transaction_type] = "SIP"), [amount]) / 10000000

Total Folios = DISTINCTCOUNT(Investor Transactions[investor_id])

Total Schemes = DISTINCTCOUNT(Scheme Performance[scheme_name])

Avg Sharpe = AVERAGE(Fund Scorecard[sharpe_ratio])

Avg Fund Score = AVERAGE(Fund Scorecard[fund_score])

Monthly SIP Count = COUNTX(FILTER(Investor Transactions, [transaction_type] = "SIP"), Investor Transactions[investor_id])

Total Transaction Amount = SUM(Investor Transactions[amount])

Avg Portfolio Value = AVERAGE(Investor Transactions[amount])

Category Concentration = SUMX(FILTER(Scheme Performance, [category] = SELECTEDVALUE(Scheme Performance[category])), [AUM])
```

---

## TROUBLESHOOTING

### Issue: Tables not showing relationships
**Solution:** 
1. Go to Model view
2. Verify all 8 tables are present
3. Drag amfi_code/date from Scheme Performance to related tables
4. Set Cardinality: Many-to-One

### Issue: Slicers not filtering charts
**Solution:**
1. Select slicer
2. Right-click > Edit interactions
3. Set interaction to "Filter"
4. Repeat for each chart on page

### Issue: Missing data in charts
**Solution:**
1. Check filters/slicers (remove all)
2. Verify column names match exactly (case-sensitive)
3. Check data types (dates should be Date, numbers should be Numeric)

### Issue: Performance slow
**Solution:**
1. Reduce data rows: Filter to top 1,000 schemes only
2. Hide unused columns in each table
3. Use aggregated tables instead of raw transactions for trends

---

## ESTIMATED TIME BREAKDOWN

- **Data Import & Setup:** 5 min
- **Create Measures:** 3 min
- **Page 1 (Overview):** 4 min
- **Page 2 (Performance):** 5 min
- **Page 3 (Investor):** 5 min
- **Page 4 (SIP Trends):** 5 min
- **Branding & Formatting:** 2 min
- **Interactivity:** 2 min
- **Export:** 3 min
- **Buffer/Testing:** 3 min
- **TOTAL:** ~37 min (realistic 45 min with testing)

---

## NEXT STEPS

1. ✅ Open Power BI Desktop
2. ✅ Follow Section 1 (Data Import) — 5 minutes
3. ✅ Create all measures from Section 2 — 3 minutes
4. ✅ Build Page 1 using Section 3 — 4 minutes
5. ✅ Build Page 2 using Section 4 — 5 minutes
6. ✅ Build Page 3 using Section 5 — 5 minutes
7. ✅ Build Page 4 using Section 6 — 5 minutes
8. ✅ Apply branding from Section 7 — 2 minutes
9. ✅ Add interactivity from Section 8 — 2 minutes
10. ✅ Export following Section 9 — 3 minutes

**You're ready to go!** 🚀
