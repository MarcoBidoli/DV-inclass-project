import pandas as pd

# 1. Load the original data
df = pd.read_csv("data/fuel_prices.csv")

# 2. Define the fuel types you want to keep
target_fuels = ['Benzina', 'Gasolio']

# 3. Filter the DataFrame
df_filtered = df[df['descCarburante'].isin(target_fuels)]

# 4. Save to a new CSV file
df_filtered.to_csv("data/filtered_fuel_prices_italy_20200101-20260331.csv", index=False)

print(f"Done! New file saved with {len(df_filtered)} rows.")