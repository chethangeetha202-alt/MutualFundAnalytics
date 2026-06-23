import pandas as pd
import os

folder = "data/raw"

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        print("\n")
        print("=" * 60)
        print("FILE:", file)
        print("=" * 60)

        # Shape
        print("\nShape:")
        print(df.shape)

        # Missing Values
        print("\nMissing Values:")
        print(df.isnull().sum())

        # Duplicate Rows
        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        # Data Types
        print("\nData Types:")
        print(df.dtypes)