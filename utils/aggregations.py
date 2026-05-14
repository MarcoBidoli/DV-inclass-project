import pandas as pd

def get_regional_summary(df, year=None, fuel_type=None):
    """
    Calculates regional average price, national average, and deviation.
    """
    filtered_df = df.copy()
    if year:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if fuel_type:
        filtered_df = filtered_df[filtered_df['descCarburante'] == fuel_type]
    
    # Regional Average
    reg_avg = filtered_df.groupby(['DEN_REG', 'DEN_REG_MAPPED']).agg(
        avg_price=('prezzo', 'mean'),
        count=('prezzo', 'count')
    ).reset_index()
    
    if reg_avg.empty:
        return reg_avg
    
    # National Average (weighted by number of reports per region to be accurate, 
    # or just simple mean of all raw records for that period)
    nat_avg = filtered_df['prezzo'].mean()
    
    reg_avg['nat_avg'] = nat_avg
    reg_avg['deviation_pct'] = ((reg_avg['avg_price'] - nat_avg) / nat_avg) * 100
    reg_avg['deviation_abs'] = reg_avg['avg_price'] - nat_avg
    
    return reg_avg

def get_time_series(df, regions=None, fuel_types=None, agg_level='monthly'):
    """
    Calculates time series data for line charts.
    """
    filtered_df = df.copy()
    if regions:
        filtered_df = filtered_df[filtered_df['DEN_REG'].isin(regions)]
    if fuel_types:
        filtered_df = filtered_df[filtered_df['descCarburante'].isin(fuel_types)]
    
    if agg_level == 'daily':
        group_cols = ['Data', 'DEN_REG', 'descCarburante']
    elif agg_level == 'monthly':
        filtered_df['Periodo'] = filtered_df['Data'].dt.to_period('M').dt.to_timestamp()
        group_cols = ['Periodo', 'DEN_REG', 'descCarburante']
    else: # yearly
        filtered_df['Periodo'] = filtered_df['Data'].dt.to_period('Y').dt.to_timestamp()
        group_cols = ['Periodo', 'DEN_REG', 'descCarburante']
        
    ts_data = filtered_df.groupby(group_cols)['prezzo'].mean().reset_index()
    
    # Also calculate national average for the same period
    if agg_level == 'daily':
        nat_cols = ['Data', 'descCarburante']
    else:
        nat_cols = ['Periodo', 'descCarburante']
        
    nat_ts = filtered_df.groupby(nat_cols)['prezzo'].mean().reset_index()
    nat_ts['DEN_REG'] = 'National Average'
    
    return pd.concat([ts_data, nat_ts])
