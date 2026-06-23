import pandas as pd
import os

folder = "data/raw"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        print("\n")
        print("="*50)
        print(file)
        print("="*50)

        print("Shape:", df.shape)
        print(df.dtypes)
        print(df.head())