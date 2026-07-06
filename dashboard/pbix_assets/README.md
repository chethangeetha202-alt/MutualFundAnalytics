Power BI dashboard assets for the mutual fund analytics project.

This folder contains the data model notes, page plan, and export instructions for the PBIX report.

Planned report pages:

1. Industry Overview
2. Fund Performance
3. Investor Analytics
4. SIP & Market Trends
5. Risk & Recommendations

Data source files:

- data/processed/nav_history_clean.csv
- data/processed/scheme_performance_clean.csv
- data/processed/investor_transactions_clean.csv
- fund_scorecard.csv
- fund_risk_profile.csv
- fund_recommendations.csv
- sector_concentration.csv
- sip_cohort_retention.csv
- sip_continuity.csv

Use the output CSVs from `build_performance_analytics.py` to enrich the Power BI visuals and support risk/recommendation dashboards.
