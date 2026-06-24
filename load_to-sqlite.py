import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bluestock_mf.db")

# Load cleaned files
nav = pd.read_csv("data/processed/nav_history_clean.csv")
txn = pd.read_csv("data/processed/investor_transactions_clean.csv")
perf = pd.read_csv("data/processed/scheme_performance_clean.csv")

# Load tables
nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
txn.to_sql("fact_transactions", engine, if_exists="replace", index=False)
perf.to_sql("fact_performance", engine, if_exists="replace", index=False)

print("SQLite database created successfully!")