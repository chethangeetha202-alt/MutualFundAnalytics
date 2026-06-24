import pandas as pd

master = pd.read_csv("data/raw/01_fund_master.csv")
nav = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(master["amfi_code"])
nav_codes = set(nav["amfi_code"])

missing_codes = master_codes - nav_codes

print("Total Fund Master Codes:", len(master_codes))
print("Total NAV History Codes:", len(nav_codes))

if len(missing_codes) == 0:
    print("\nAll AMFI codes from fund_master exist in nav_history")
else:
    print("\nMissing Codes:")
    print(missing_codes)