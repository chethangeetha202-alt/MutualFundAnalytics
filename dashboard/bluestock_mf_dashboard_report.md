# Bluestock Mutual Fund Dashboard Report

This report package contains the structure and data model needed to build the Power BI dashboard for the mutual fund analytics project.

## Included files

- Report plan: dashboard/pbix_assets/report_plan.json
- Data model: dashboard/pbix_assets/data_model.md
- Report definition: dashboard/pbix_assets/report_definition.md
- Import schema: dashboard/pbix_assets/data/schema.json

## Data sources

- data/processed/nav_history_clean.csv
- data/processed/scheme_performance_clean.csv
- data/processed/investor_transactions_clean.csv
- fund_scorecard.csv
- fund_risk_profile.csv
- fund_recommendations.csv
- sector_concentration.csv
- sip_cohort_retention.csv
- sip_continuity.csv

## Notes

- The report is organized into 5 pages: Industry Overview, Fund Performance, Investor Analytics, SIP & Market Trends, and Risk & Recommendations.
- The deliverables are ready to be opened in Power BI Desktop and saved as a PBIX file.
- Manual export is required for `.pbix`, PDF, and page PNGs because headless Power BI export is not supported in this environment.
