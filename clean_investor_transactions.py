import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/08_investor_transactions.csv")

print("Original Shape:", df.shape)

# Remove duplicates
df = df.drop_duplicates()

# Keep only positive transaction amounts
df = df[df["amount_inr"] > 0]

# Convert date column
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

print("Cleaned Shape:", df.shape)

# Save cleaned dataset
df.to_csv(
    "data/processed/investor_transactions_clean.csv",
    index=False
)

print("Investor Transactions cleaned successfully!")