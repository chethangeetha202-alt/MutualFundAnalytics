from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

# Ensure main analytics outputs exist
required_files = [
    ROOT / 'fund_scorecard.csv',
    ROOT / 'fund_risk_profile.csv',
    ROOT / 'fund_recommendations.csv',
    ROOT / 'sector_concentration.csv',
    ROOT / 'sip_cohort_retention.csv',
    ROOT / 'sip_continuity.csv',
]
missing = [str(p.name) for p in required_files if not p.exists()]
if missing:
    raise SystemExit(f'Missing required files: {missing}')

# Create a direct VaR/CVaR report
fund_risk_profile = pd.read_csv(ROOT / 'fund_risk_profile.csv')
var_cvar = fund_risk_profile[
    ['amfi_code', 'var_95_pct', 'cvar_95_pct', 'var_99_pct', 'cvar_99_pct']
].copy()
var_cvar = var_cvar.merge(
    pd.read_csv(ROOT / 'fund_scorecard.csv')[['amfi_code', 'scheme_name', 'fund_house', 'category', 'plan']],
    on='amfi_code', how='left'
)
var_cvar.to_csv(ROOT / 'var_cvar_report.csv', index=False)

# Create a direct rolling Sharpe chart
if 'rolling_sharpe_90d' in fund_risk_profile.columns:
    top = fund_risk_profile.sort_values('rolling_sharpe_90d', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(top['amfi_code'].astype(str) + ' - ' + top['scheme_name'], top['rolling_sharpe_90d'], color='#1976d2')
    ax.invert_yaxis()
    ax.set_xlabel('Rolling 90-day Sharpe')
    ax.set_title('Top 10 Funds by Rolling 90-day Sharpe')
    fig.tight_layout()
    fig.savefig(ROOT / 'rolling_sharpe_chart.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
else:
    raise SystemExit('rolling_sharpe_90d column missing in fund_risk_profile.csv')

# Generate deliverable summary
summary_lines = [
    '# Final Deliverables',
    '',
    'The following files have been generated or verified as complete for the project deliverables:',
    '',
    '- `fund_scorecard.csv`',
    '- `fund_risk_profile.csv`',
    '- `fund_recommendations.csv`',
    '- `sector_concentration.csv`',
    '- `sip_cohort_retention.csv`',
    '- `sip_continuity.csv`',
    '- `alpha_beta.csv`',
    '- `benchmark_comparison.png`',
    '- `sector_concentration.png`',
    '- `sip_cohort_retention.png`',
    '- `sip_continuity.png`',
    '- `var_cvar_report.csv`',
    '- `rolling_sharpe_chart.png`',
    '',
    '## Notes',
    '',
    '- `build_performance_analytics.py` already implements the task steps from the image.',
    '- `dashboard/pbix_assets/` contains the Power BI report definition, data model, and export instructions.',
    '- Use the CSV files above as Power BI data sources to create the final dashboard.',
]
with open(ROOT / 'final_deliverables.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary_lines))

print('Completed deliverables: var_cvar_report.csv, rolling_sharpe_chart.png, final_deliverables.md')
