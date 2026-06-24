# Mutual Fund Analytics Data Dictionary

## Fund Master

- amfi_code : Unique mutual fund identifier
- scheme_name : Name of scheme
- fund_house : Mutual fund company
- category : Equity/Debt
- sub_category : Fund subtype
- risk_category : Risk level

## NAV History

- amfi_code : Fund identifier
- date : NAV date
- nav : Net Asset Value

## Investor Transactions

- investor_id : Investor identifier
- transaction_date : Date of transaction
- transaction_type : SIP/Lumpsum/Redemption
- amount_inr : Transaction amount

## Scheme Performance

- return_1yr_pct : 1 year return
- return_3yr_pct : 3 year return
- return_5yr_pct : 5 year return
- expense_ratio_pct : Expense ratio
- aum_crore : Assets under management
