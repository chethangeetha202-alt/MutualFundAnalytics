import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

data = response.json()

print("Fund Name:", data["meta"]["scheme_name"])

nav_df = pd.DataFrame(data["data"])

nav_df.to_csv("data/raw/hdfc_top100_nav.csv", index=False)

print("CSV saved successfully!")

import requests
import pandas as pd

scheme_code = 125497

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)

data = response.json()

nav_df = pd.DataFrame(data["data"])

nav_df.to_csv(
    "data/raw/live_nav.csv",
    index=False
)

print("Downloaded")