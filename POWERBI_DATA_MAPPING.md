# Power BI Data Mapping & Import Guide

## Complete Data Structure Reference

This guide shows exactly what's in each CSV file, column names, sample data, and how they connect.

---

## TABLE 1: Scheme Performance (MAIN TABLE)

**File Location:** `data/processed/scheme_performance_clean.csv`

### Columns & Data Types

| Column Name | Data Type | Sample Value | Use In |
|-------------|-----------|--------------|--------|
| amfi_code | Integer | 120302 | Link to NAV, Transactions, Scorecard |
| scheme_name | Text | "ICICI Pru Midcap Fund - Regular" | Display in charts |
| category | Text | "Mid Cap" | Slicer, bar/pie charts |
| fund_house | Text | "ICICI Prudential" | Charts, KPI |
| expense_ratio | Decimal | 1.25 | Fund scorecard column |
| aum | Currency | 18500000000 | AUM KPI, bubble size |
| plan_type | Text | "Regular" / "Direct" | Slicer |
| launch_date | Date | 2015-03-20 | Reference |

### Row Count: 40 funds

---

## TABLE 2: NAV History (Daily NAV Data)

**File Location:** `data/processed/nav_history_clean.csv`

### Columns & Data Types

| Column Name | Data Type | Sample Value | Use In |
|-------------|-----------|--------------|--------|
| amfi_code | Integer | 120302 | Link to Scheme Performance |
| date | Date | 2023-01-03 | X-axis in charts, daily performance |
| nav | Currency | 145.32 | Line chart, trend analysis |

### Row Count: ~46,251 records (1,000+ per fund)

---

## TABLE 3: Investor Transactions

**File Location:** `data/processed/investor_transactions_clean.csv`

### Columns & Data Types

| Column Name | Data Type | Sample Value | Use In |
|-------------|-----------|--------------|--------|
| investor_id | Text | "INV_12345" | Distinct count for folios |
| amfi_code | Integer | 120302 | Link to Scheme Performance |
| transaction_date | Date | 2024-02-15 | Monthly trends, timeline |
| amount | Currency | 50000 | Sum for KPIs, bar charts |
| transaction_type | Text | "SIP" / "Lumpsum" / "Redemption" | Donut chart filter |
| state | Text | "Maharashtra" | State-wise analysis slicer |
| age_group | Text | "25-35" | Age group bar chart |
| city_tier | Text | "Tier 1" / "Tier 2" / "Tier 3" | City tier slicer |

### Row Count: ~1,362 investors (variable transactions each)

---

## TABLE 4: Fund Scorecard

**File Location:** `fund_scorecard.csv` (Root directory)

### Columns & Data Types

| Column Name | Data Type | Sample Value |
|-------------|-----------|--------------|
| scheme_name | Text | "ICICI Pru Midcap Fund - Regular" |
| amfi_code | Integer | 120302 |
| fund_score | Decimal | 84.1 |
| cagr_3yr | Decimal | 0.3174 |
| sharpe_ratio | Decimal | 1.1806 |
| alpha | Decimal | 0.2926 |
| beta | Decimal | 0.0005 |
| max_drawdown | Decimal | -0.2306 |

### Row Count: 40 funds

---

## TABLE 5: Alpha Beta

**File Location:** `alpha_beta.csv` (Root directory)

### Columns & Data Types

| Column Name | Data Type | Sample Value |
|-------------|-----------|--------------|
| scheme_name | Text | "ICICI Pru Midcap Fund - Regular" |
| alpha | Decimal | 0.2926 |
| beta | Decimal | 0.0005 |
| tracking_error_nifty100 | Decimal | 0.2319 |

### Row Count: 40 funds

---

## TABLE 6: Fund Risk Profile

**File Location:** `fund_risk_profile.csv` (Root directory)

### Columns & Data Types

| Column Name | Data Type | Sample Value |
|-------------|-----------|--------------|
| scheme_name | Text | "ICICI Pru Midcap Fund - Regular" |
| risk_grade | Text | "Moderate" / "High" / "Low" |

### Row Count: 40 funds

---

## TABLE 7: AUM by Fund House

**File Location:** `data/raw/03_aum_by_fund_house.csv`

### Columns & Data Types

| Column Name | Data Type | Sample Value |
|-------------|-----------|--------------|
| fund_house | Text | "ICICI Prudential" |
| date | Date | 2022-01-31 |
| aum | Currency | 8500000000 |

### Row Count: ~200 records (fund houses × months)

---

## TABLE 8: Benchmark Indices

**File Location:** `data/raw/10_benchmark_indices.csv`

### Columns & Data Types

| Column Name | Data Type | Sample Value |
|-------------|-----------|--------------|
| date | Date | 2023-01-03 |
| nifty_50 | Decimal | 59123.45 |
| nifty_100 | Decimal | 21450.32 |

### Row Count: ~1,000 records (daily index values)

---

## IMPORT PROCEDURE

### Step 1: Import Main Table
```
1. Power BI Desktop > Home > Get Data > Text/CSV
2. Select: data/processed/scheme_performance_clean.csv
3. Load
```

### Step 2: Import Related Tables
For each of the remaining 7 tables:
```
1. Home > Get Data > Text/CSV
2. Select file > Load
```

### Step 3: Create Relationships
Navigate to Model view and link:
- Scheme Performance[amfi_code] ← NAV History[amfi_code]
- Scheme Performance[amfi_code] ← Investor Transactions[amfi_code]
- Scheme Performance[amfi_code] ← Fund Scorecard[amfi_code]
- Scheme Performance[scheme_name] ← Alpha Beta[scheme_name]
- Scheme Performance[amfi_code] ← Fund Risk Profile[amfi_code]
- Scheme Performance[fund_house] ← AUM by Fund House[fund_house]
- NAV History[date] ← Benchmark Indices[date]

For each: Right-click > Edit > Cardinality: Many-to-One > Cross-filter: Both > OK

---

**Full import guide with troubleshooting:** See POWERBI_IMPLEMENTATION_GUIDE.md
