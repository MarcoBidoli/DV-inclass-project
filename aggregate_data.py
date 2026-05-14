import pandas as pd
import glob
import os
import numpy as np

files = sorted(glob.glob('prezzi_daily_by_year/*.csv'))
output_file = 'summary_data.csv'
dist_output_file = 'distribution_data.csv'

def process_data(files):
    summaries = []
    distribution_samples = []
    
    for f in files:
        print(f"Processing {f}...")
        chunks = pd.read_csv(f, usecols=['Data', 'DEN_REG', 'descCarburante', 'prezzo', 'year'], chunksize=1000000)
        for chunk in chunks:
            # 0.1% sample for distribution
            dist_sample = chunk.sample(frac=0.001, random_state=42)
            distribution_samples.append(dist_sample)
            
            # Full aggregation for choropleth
            chunk['Data'] = pd.to_datetime(chunk['Data'])
            chunk['month'] = chunk['Data'].dt.month
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
