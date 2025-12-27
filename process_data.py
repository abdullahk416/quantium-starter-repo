import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

files = [
    DATA_DIR / "daily_sales_data_0.csv",
    DATA_DIR / "daily_sales_data_1.csv",
    DATA_DIR / "daily_sales_data_2.csv",
]

dataframes = []

for file in files:
    df = pd.read_csv(file)
    
    # include only pink morsels 
    df = df[df["product"] == "pink morsel"].copy()
    
    # remove dollar sign from price column
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
    
    # create Sales column
    df["Sales"] = df["price"] * df["quantity"] 
    
    # include only required columns
    df = df[["Sales", "date", "region"]] 
    
    # rename columns for grammer
    df = df.rename(columns={
        "date": "Date",
        "region": "Region"
    })
    
    dataframes.append(df) 
    
final_df = pd.concat(dataframes, ignore_index=True)

final_df.to_csv("formatted_sales_data.csv", index=False)
