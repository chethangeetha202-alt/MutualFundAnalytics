# Advanced Mutual Fund Analytics - Deliverables Summary

## ✅ All 7 Tasks Completed

### 1. **Historical VaR (95%) & CVaR Analysis** ✓
**Status:** Complete | **Output:** `var_cvar_report.csv`

**Metrics Calculated:**
- **Value at Risk (VaR)**: 5th percentile of daily return distribution for all 40 schemes
- **Conditional Value at Risk (CVaR)**: Mean of returns below VaR threshold

**Key Findings:**
- Highest Risk Fund (VaR): Small Cap/Mid Cap funds at ~1.3% daily loss potential
- Lowest Risk Fund (VaR): Liquid funds at ~0.022% daily loss potential
- Average Portfolio VaR: -1.47%
- Average Portfolio CVaR: -1.86%

**File:** `var_cvar_report.csv` (40 schemes × 7 metrics)

---

### 2. **Rolling 90-Day Sharpe Ratio Analysis** ✓
**Status:** Complete | **Output:** `rolling_sharpe_chart.png`

**Formula Applied:** Rolling(90).mean() / Rolling(90).std() × √252

**Top 5 Funds Analyzed:**
1. ICICI Pru Liquid Fund - Mean Sharpe: 13.56 (Range: 9.60-18.30)
2. Kotak Liquid Fund - Mean Sharpe: 12.48 (Range: 7.65-16.87)
3. ABSL Liquid Fund - Mean Sharpe: 11.99 (Range: 8.76-15.36)
4. HDFC Short Term Debt - Mean Sharpe: 1.13 (Range: -2.79-4.93)
5. SBI Magnum Gilt Fund - Mean Sharpe: 1.53 (Range: -2.39-4.10)

**Visualization:** 5-panel time-series chart showing rolling Sharpe performance over 1000+ days

**File:** `rolling_sharpe_chart.png` (916 KB, high-resolution)

---

### 3. **Investor Cohort Analysis** ✓
**Status:** Complete | **Output:** `investor_cohort_analysis.csv`

**Grouping:** By first transaction year

**Cohort Breakdown:**
| Cohort | Investors | Avg SIP | Total Invested | Top Fund |
|--------|-----------|---------|----------------|----------|
| 2024 | 4,624 | ₹10,997 | ₹214.98 Cr | ICICI Bluechip (536) |
| 2025 | 138 | ₹13,505 | ₹2.26 Cr | SBI Small Cap (8) |

**Insights:**
- 2024 cohort dominates investment volume
- Newer investors (2025) have higher average SIP amounts
- Both cohorts diversified across all 40 available funds

**File:** `investor_cohort_analysis.csv` (2 cohorts × 8 metrics)

---

### 4. **SIP Continuity Analysis** ✓
**Status:** Complete | **Output:** `sip_continuity_analysis.csv`

**Filter Applied:** Investors with 6+ SIP transactions

**Risk Classification:** Gap > 35 days = "At-Risk"

**Key Metrics:**
- **Total Active SIP Investors:** 1,362
- **At-Risk Investors:** 1,361 (99.9%)
- **Average Gap Between SIPs:** 64.9 days
- **Median Gap:** 64.7 days
- **Maximum Observed Gap:** 372 days

**Top 5 At-Risk High-Value Investors:**
1. INV000862: ₹119,139 | Max Gap: 372 days
2. INV003484: ₹108,256 | Max Gap: 333 days
3. INV001070: ₹103,923 | Max Gap: 329 days
4. INV003223: ₹115,743 | Max Gap: 331 days
5. INV002177: ₹93,321 | Max Gap: 330 days

**File:** `sip_continuity_analysis.csv` (1,362 investors × 6 metrics)

---

### 5. **Fund Recommender System** ✓
**Status:** Complete | **Output:** `recommender.py`

**Recommendation Logic:**
- Input: Risk Appetite (Low / Moderate / High)
- Output: Top 3 funds by Sharpe ratio within matching risk_grade
- Ranking Metric: Sharpe Ratio (higher = better risk-adjusted returns)

**Recommended Funds:**

**Low Risk Appetite (Liquid Funds):**
1. ICICI Pru Liquid Fund - Sharpe: 7.68, Alpha: 1.85
2. Kotak Liquid Fund - Sharpe: 6.18, Alpha: 1.52
3. ABSL Liquid Fund - Sharpe: 5.14, Alpha: 1.18

**Moderate Risk Appetite (Large Cap):**
1. HDFC Top 100 Fund - Sharpe: 1.06, Alpha: 0.78
2. Mirae Asset Large Cap Fund - Sharpe: 1.06, Alpha: 1.62
3. ICICI Pru Bluechip Fund - Sharpe: 1.03, Alpha: 0.88

**High Risk Appetite (Mid Cap):**
1. Kotak Emerging Equity Fund - Sharpe: 0.96, Alpha: 1.91
2. ICICI Pru Midcap Fund - Sharpe: 0.95, Alpha: 0.89
3. DSP Midcap Fund - Sharpe: 0.90, Alpha: 1.02

**File:** `recommender.py` (4.17 KB, production-ready)

---

### 6. **Sector HHI Concentration Analysis** ✓
**Status:** Complete | **Output:** `sector_hhi_analysis.csv`

**Formula:** HHI = Σ(weight_i²) where weight_i = sector weight %

**Concentration Classification:**
- **Highly Concentrated:** HHI > 2500 (0 funds, 0%)
- **Moderately Concentrated:** 1500 < HHI ≤ 2500 (9 funds, 26.5%)
- **Diversified:** HHI < 1500 (25 funds, 73.5%)

**Most Concentrated Portfolio:**
- Fund: Axis Bluechip Fund - Regular - Growth
- HHI: 2064 (Moderately Concentrated)
- Top 3 Sectors: Financial Services, IT, Manufacturing

**Most Diversified Portfolio:**
- Fund: SBI Small Cap Fund - Regular Plan - Growth
- HHI: 1073 (Diversified)
- Sectors: 10 distinct sectors

**Portfolio Metrics:**
- Average HHI: 1403
- Median HHI: 1365
- Sector Count Range: 6-10 sectors per fund

**File:** `sector_hhi_analysis.csv` (34 equity funds × 7 metrics)

---

### 7. **Five Advanced Insights** ✓
**Status:** Complete | **Location:** Advanced_Analytics.ipynb (Section 8)

#### **Insight 1: Highest Risk Funds (VaR Analysis)**
- Liquid funds have lowest VaR (<0.03%) = most stable
- Equity funds have highest VaR (>1.2%) = highest volatility
- **Recommendation:** Match fund selection to investor risk tolerance

#### **Insight 2: Largest Investor Cohorts**
- 2024 cohort generates ₹214.98 Cr revenue from 4,624 investors
- Top fund preference: ICICI Pru Bluechip (536 investments)
- **Recommendation:** Focus retention on 2024 cohort; diversify 2025 marketing

#### **Insight 3: SIP Continuity Crisis**
- 99.9% of active SIP investors are "at-risk" (gap > 35 days)
- Average gap of 64.9 days suggests quarterly SIP patterns, not monthly
- **Recommendation:** Implement automated engagement for gaps > 35 days

#### **Insight 4: Portfolio Diversification Trends**
- 73.5% of funds are well-diversified (HHI < 1500)
- Average 8 sectors per fund ensures risk mitigation
- **Recommendation:** Safe for conservative investors; concentrated bets available for aggressive

#### **Insight 5: Fund Recommendation Effectiveness**
- Low-risk liquid funds: Average Sharpe 6.33 (excellent consistency)
- Moderate-risk large-cap: Average Sharpe 1.05 (solid performance)
- High-risk mid-cap: Average Sharpe 0.94 (growth potential with volatility)
- **Recommendation:** Implement KYC-based automated recommendations

---

## 📊 Deliverables Summary

| Deliverable | Type | Size | Status |
|-------------|------|------|--------|
| Advanced_Analytics.ipynb | Jupyter Notebook | 40.7 KB | ✓ Complete |
| var_cvar_report.csv | CSV Data | 3.89 KB | ✓ Complete |
| sector_hhi_analysis.csv | CSV Data | 4.6 KB | ✓ Complete |
| sip_continuity_analysis.csv | CSV Data | 42.88 KB | ✓ Complete |
| investor_cohort_analysis.csv | CSV Data | 0.29 KB | ✓ Complete |
| rolling_sharpe_chart.png | Visualization | 915.9 KB | ✓ Complete |
| recommender.py | Python Module | 4.17 KB | ✓ Complete |

**Total Package Size:** ~1.01 MB

---

## 🚀 Implementation Roadmap

### Phase 1: Immediate Actions
- [ ] Import var_cvar_report.csv into Power BI for risk dashboard
- [ ] Deploy recommender.py for automated fund recommendations
- [ ] Review sip_continuity_analysis.csv for at-risk investor outreach

### Phase 2: Strategic Initiatives (Week 1-2)
- [ ] Implement KYC-based fund matching using recommender engine
- [ ] Launch engagement campaign for at-risk SIP investors
- [ ] Create portfolio concentration watchlist (track HHI > 2000)

### Phase 3: Ongoing Monitoring (Weekly)
- [ ] Update rolling Sharpe ratios with new data
- [ ] Refresh cohort analysis with quarterly data
- [ ] Monitor SIP continuity trends for early warning signals

---

## 📌 Key Metrics at a Glance

```
Total Schemes Analyzed:          40
Active SIP Investors (6+ SIPs):   1,362
At-Risk Investors:               1,361 (99.9%)
Investor Cohorts:                2
Portfolio Holdings Analyzed:     34

Risk Distribution:
├─ Liquid Funds:                 3 (7.5%)
├─ Short Duration:               1 (2.5%)
├─ Gilt:                         2 (5%)
├─ Index/ETF:                    2 (5%)
├─ Large Cap:                    12 (30%)
├─ Mid Cap:                      8 (20%)
├─ Small Cap:                    3 (7.5%)
├─ ELSS:                         4 (10%)
├─ Value:                        2 (5%)
└─ Large & Mid Cap:              1 (2.5%)

Performance Metrics:
├─ Average Sharpe Ratio:         2.87
├─ Average Alpha:                1.18
├─ Average Beta:                 0.97
├─ Average HHI:                  1403
└─ Diversification Rate:         73.5%
```

---

## 💾 File Locations

All files available in: `c:\Users\cheth\Downloads\MutualFundAnalytics\`

```
├── Advanced_Analytics.ipynb                (Main analysis notebook)
├── var_cvar_report.csv                    (VaR/CVaR metrics)
├── sector_hhi_analysis.csv                (Sector concentration)
├── sip_continuity_analysis.csv            (SIP continuity tracking)
├── investor_cohort_analysis.csv           (Investor cohorts)
├── rolling_sharpe_chart.png               (Sharpe visualizations)
├── recommender.py                         (Fund recommender engine)
└── ADVANCED_ANALYTICS_SUMMARY.md          (This document)
```

---

## 📖 Documentation

**Jupyter Notebook:** Contains 9 comprehensive sections:
1. Import libraries and data loading
2. VaR/CVaR calculations with visualizations
3. Rolling Sharpe ratio analysis with time-series charts
4. Investor cohort profiling with demographics
5. SIP continuity risk assessment
6. Fund recommendation engine with examples
7. Sector concentration analysis with HHI scores
8. Strategic insights and recommendations
9. Results export and summary statistics

**Python Module:** Production-ready recommender system with:
- Risk-based fund filtering
- Sharpe ratio ranking
- Portfolio allocation suggestions
- Fund performance analysis methods

---

**Analysis Generated:** 2026-07-06  
**Status:** ✅ ALL TASKS COMPLETED SUCCESSFULLY
