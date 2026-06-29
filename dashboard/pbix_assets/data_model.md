Power BI data model outline

Tables to import from CSV files:

- nav_history_clean.csv
  - amfi_code
  - date
  - nav
- scheme_performance_clean.csv
  - amfi_code
  - scheme_name
  - fund_house
  - category
  - plan
  - return_1yr_pct
  - return_3yr_pct
  - return_5yr_pct
  - expense_ratio_pct
  - aum_crore
  - benchmark_3yr_pct
- investor_transactions_clean.csv
  - investor_id
  - transaction_date
  - amfi_code
  - transaction_type
  - amount_inr
  - state
  - city
  - city_tier
  - age_group
  - gender
  - annual_income_lakh
  - payment_mode
  - kyc_status

Relationships:

- nav_history_clean.amfi_code -> scheme_performance_clean.amfi_code
- nav_history_clean.date -> transaction_date (for time-based visuals)
- investor_transactions_clean.amfi_code -> scheme_performance_clean.amfi_code
