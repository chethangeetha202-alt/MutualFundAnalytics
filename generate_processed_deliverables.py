from pathlib import Path
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
PROC = ROOT / 'data' / 'processed'
PROC.mkdir(parents=True, exist_ok=True)

# Core cleaned exports
fund_master = pd.read_csv(RAW / '01_fund_master.csv')
nav_history_data = pd.read_csv(RAW / '02_nav_history.csv')
performance = pd.read_csv(RAW / '07_scheme_performance.csv')
transactions = pd.read_csv(RAW / '08_investor_transactions.csv')
portfolio = pd.read_csv(RAW / '09_portfolio_holdings.csv')

nav_clean = nav_history_data.copy()
if 'date' in nav_clean.columns:
    nav_clean['date'] = pd.to_datetime(nav_clean['date'], errors='coerce')
nav_clean = nav_clean.sort_values(['amfi_code', 'date']) if {'amfi_code', 'date'}.issubset(nav_clean.columns) else nav_clean
nav_clean = nav_clean.drop_duplicates()
if 'nav' in nav_clean.columns:
    nav_clean = nav_clean[nav_clean['nav'] > 0]
nav_clean.to_csv(PROC / 'nav_history_clean.csv', index=False)

transactions_clean = transactions.copy()
if 'transaction_type' in transactions_clean.columns:
    transactions_clean['transaction_type'] = transactions_clean['transaction_type'].astype(str).str.strip().str.title()
    transactions_clean.loc[transactions_clean['transaction_type'].isin(['Sip', 'Sips']), 'transaction_type'] = 'SIP'
    transactions_clean.loc[transactions_clean['transaction_type'].isin(['Lumpsum', 'Lump Sum']), 'transaction_type'] = 'Lumpsum'
    transactions_clean.loc[transactions_clean['transaction_type'].isin(['Redemption', 'Redeem']), 'transaction_type'] = 'Redemption'
if 'amount_inr' in transactions_clean.columns:
    transactions_clean['amount_inr'] = pd.to_numeric(transactions_clean['amount_inr'], errors='coerce')
    transactions_clean = transactions_clean[transactions_clean['amount_inr'] > 0]
if 'transaction_date' in transactions_clean.columns:
    transactions_clean['transaction_date'] = pd.to_datetime(transactions_clean['transaction_date'], errors='coerce')
transactions_clean.to_csv(PROC / 'investor_transactions_clean.csv', index=False)

performance_clean = performance.copy()
for col in ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct', 'aum_crore']:
    if col in performance_clean.columns:
        performance_clean[col] = pd.to_numeric(performance_clean[col], errors='coerce')
performance_clean = performance_clean[performance_clean['amfi_code'].notna()].copy()
performance_clean.to_csv(PROC / 'scheme_performance_clean.csv', index=False)

fund_master.to_csv(PROC / 'fund_master_clean.csv', index=False)
portfolio.to_csv(PROC / 'portfolio_holdings_clean.csv', index=False)

# Copy the main analysis outputs if already present
for name in [
    'fund_scorecard.csv',
    'fund_risk_profile.csv',
    'fund_recommendations.csv',
    'sector_concentration.csv',
    'sip_cohort_retention.csv',
    'sip_continuity.csv',
    'alpha_beta.csv',
    'var_cvar_report.csv',
]:
    src = ROOT / name
    if src.exists():
        shutil.copy2(src, PROC / name)

print('Processed deliverables generated in', PROC)
print([p.name for p in sorted(PROC.glob('*.csv'))])
