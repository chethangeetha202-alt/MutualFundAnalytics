import json
from pathlib import Path
import pandas as pd

root = Path('.')
files = ['Performance_Analytics.ipynb', 'fund_scorecard.csv', 'alpha_beta.csv', 'benchmark_comparison.png', 'benchmark_comparison_chart.png']
for path in files:
    p = root / path
    print(path, 'exists=', p.exists(), 'size=', p.stat().st_size if p.exists() else None)

with open('Performance_Analytics.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
print('notebook cells=', len(nb['cells']))
scorecard = pd.read_csv('fund_scorecard.csv')
alpha_beta = pd.read_csv('alpha_beta.csv')
print('scorecard shape=', scorecard.shape)
print('alpha_beta shape=', alpha_beta.shape)
print('top1=', scorecard.loc[0, 'scheme_name'], scorecard.loc[0, 'fund_score'])
