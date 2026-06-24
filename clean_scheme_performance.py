import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Original Shape:", df.shape)

# Remove duplicates
df = df.drop_duplicates()

# Keep valid expense ratios (0% to 2.5%)
df = df[
    (df["expense_ratio_pct"] >= 0) &
    (df["expense_ratio_pct"] <= 2.5)
]

# Keep positive AUM
df = df[df["aum_crore"] > 0]

print("Cleaned Shape:", df.shape)

# Save cleaned file
df.to_csv(
    "data/processed/scheme_performance_clean.csv",
    index=False
)

print("Scheme Performance cleaned successfully!")