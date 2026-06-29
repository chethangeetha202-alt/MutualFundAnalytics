import pandas as pd

nav = pd.read_csv('data/raw/02_nav_history.csv')
perf = pd.read_csv('data/raw/07_scheme_performance.csv')
bench = pd.read_csv('data/raw/10_benchmark_indices.csv')

nav['date'] = pd.to_datetime(nav['date'])
perf['amfi_code'] = perf['amfi_code'].astype(int)

print('nav rows', len(nav), 'unique funds', nav['amfi_code'].nunique())
print('perf rows', len(perf), 'unique funds', perf['amfi_code'].nunique())
print('bench rows', len(bench), 'indices', sorted(bench['index_name'].unique().tolist()))
print('nav date range', nav['date'].min(), nav['date'].max())
print('bench date range', pd.to_datetime(bench['date']).min(), pd.to_datetime(bench['date']).max())
print('sample perf amfi', perf['amfi_code'].head().tolist())
print('sample nav amfi', nav['amfi_code'].head().tolist())
