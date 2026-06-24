import pandas as pd

# Load NAV history dataset
df = pd.read_csv("data/raw/02_nav_history.csv")

print("Original Shape:", df.shape)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by amfi_code and date
df = df.sort_values(["amfi_code", "date"])

# Remove duplicate rows
df = df.drop_duplicates()

# Keep only positive NAV values
df = df[df["nav"] > 0]

print("Cleaned Shape:", df.shape)

# Save cleaned file
df.to_csv("data/processed/nav_history_clean.csv", index=False)

print("Cleaned NAV history saved successfully!")