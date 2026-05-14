import pandas as pd
import glob
import os
import numpy as np

# Check for source files
if os.path.exists('prezzi_daily_by_year'):
    files = sorted(glob.glob('prezzi_daily_by_year/*.csv'))
elif os.path.exists('gas_prices_2020Q1_to_2026Q1.csv'):
    files = ['gas_prices_2020Q1_to_2026Q1.csv']
else:
    files = []

output_file = 'summary_data.csv'
dist_output_file = 'distribution_data.csv'

def process_data(files):
    if not files:
        print("No input files found.")
        return pd.DataFrame(), pd.DataFrame()
    
    summaries = []
    distribution_samples = []
    
    for f in files:
        print(f"Processing {f}...")
        # Check columns first
        sample = pd.read_csv(f, nrows=1)
        use_cols = ['Data', 'descCarburante', 'prezzo']
        if 'DEN_REG' in sample.columns:
            use_cols.append('DEN_REG')
        elif 'Regione' in sample.columns:
            use_cols.append('Regione')
            
        chunks = pd.read_csv(f, usecols=use_cols, chunksize=1000000)
        for chunk in chunks:
            if 'Regione' in chunk.columns:
                chunk = chunk.rename(columns={'Regione': 'DEN_REG'})
            
            chunk['Data'] = pd.to_datetime(chunk['Data'])
            chunk['year'] = chunk['Data'].dt.year
            chunk['month'] = chunk['Data'].dt.month
            
            # 0.1% sample for distribution
            dist_sample = chunk.sample(frac=0.001, random_state=42)
            distribution_samples.append(dist_sample)
            
            # Full aggregation for choropleth
            agg = chunk.groupby(['year', 'month', 'DEN_REG', 'descCarburante']).agg(
                sum_prezzo=('prezzo', 'sum'),
                count_prezzo=('prezzo', 'count')
            ).reset_index()
            summaries.append(agg)
            
    print("Finalizing aggregation...")
    final = pd.concat(summaries)
    final = final.groupby(['year', 'month', 'DEN_REG', 'descCarburante']).agg(
        sum_prezzo=('sum_prezzo', 'sum'),
        count_prezzo=('count_prezzo', 'sum')
    ).reset_index()
    final['mean_prezzo'] = final['sum_prezzo'] / final['count_prezzo']
    
    dist_df = pd.concat(distribution_samples)
    dist_df['Data'] = pd.to_datetime(dist_df['Data'])
    dist_df['month'] = dist_df['Data'].dt.month
    
    return final, dist_df

final_df, dist_df = process_data(files)
final_df.to_csv(output_file, index=False)
dist_df.to_csv(dist_output_file, index=False)
print(f"Saved summary to {output_file} and distribution sample to {dist_output_file}")
