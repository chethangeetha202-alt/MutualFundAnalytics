# Mutual Fund Analytics

Bluestock Fintech Capstone Project

## Overview

This repository contains a mutual fund analytics pipeline for cleaned mutual fund data, investor transactions, benchmark indices, and portfolio holdings.

The project includes:

- `build_performance_analytics.py`: Generates fund performance scorecards, risk profiles, sector concentration, SIP cohort analytics, and recommendations.
- `data/processed/`: Cleaned input tables used for metrics and Power BI reporting.
- `dashboard/pbix_assets/`: Power BI report plan, data model notes, schema, and export instructions.
- `fund_scorecard.csv`, `fund_risk_profile.csv`, `fund_recommendations.csv`, `sector_concentration.csv`, `sip_cohort_retention.csv`, `sip_continuity.csv`: output files used by the dashboard.

## How to run

1. Activate the Python environment.
2. Run:

```powershell
python build_performance_analytics.py
```

3. This will generate CSV outputs and chart PNGs in the repository root.

## Dashboard deliverables

- Power BI dashboard plan and schema are in `dashboard/pbix_assets/`.
- Manual Power BI export is required to produce `.pbix`, PDF, and page PNGs.

## Notes

- The project now includes advanced analytics: VaR/CVaR, rolling Sharpe, SIP cohort retention, SIP continuity, sector concentration (HHI), and fund risk-based recommendations.
- If Power BI Desktop is available, import the CSV files listed in `dashboard/pbix_assets/README.md` and save the report as `bluestock_mf_dashboard.pbix`.
