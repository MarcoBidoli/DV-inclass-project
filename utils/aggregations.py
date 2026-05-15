import pandas as pd

def get_regional_summary(df, month=None, year=None, fuel_type=None, start_date=None, end_date=None):
    """
    Calculates regional average price, national average, and deviation.
    Supports filtering by month/year, or a date range.
    fuel_type can be a string or a list of strings.
    """
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]
    elif month and year:
        filtered_df = filtered_df[(filtered_df['year'] == year) & (filtered_df['month'] == month)]
    elif year:
        filtered_df = filtered_df[filtered_df['year'] == year]
    
    if fuel_type:
        if isinstance(fuel_type, list):
            filtered_df = filtered_df[filtered_df['descCarburante'].isin(fuel_type)]
        else:
            filtered_df = filtered_df[filtered_df['descCarburante'] == fuel_type]
    
    if filtered_df.empty:
        return pd.DataFrame(columns=['Regione', 'REG_MAPPED', 'descCarburante', 'avg_price', 'count', 'nat_avg', 'deviation_pct', 'deviation_abs'])
    
    # Regional Average per fuel type
    reg_avg = filtered_df.groupby(['Regione', 'REG_MAPPED', 'descCarburante']).agg(
        avg_price=('prezzo', 'mean'),
        count=('prezzo', 'count')
    ).reset_index()
    
    # National Average per fuel type
    nat_avg_map = filtered_df.groupby('descCarburante')['prezzo'].mean().to_dict()
    
    reg_avg['nat_avg'] = reg_avg['descCarburante'].map(nat_avg_map)
    reg_avg['deviation_pct'] = ((reg_avg['avg_price'] - reg_avg['nat_avg']) / reg_avg['nat_avg']) * 100
    reg_avg['deviation_abs'] = reg_avg['avg_price'] - reg_avg['nat_avg']
    
    return reg_avg

def get_time_series(df, regions=None, fuel_types=None, agg_level='weekly', start_date=None, end_date=None):
    """
    Calculates time series data for line charts.
    If regions is None, calculates national average.
    """
    filtered_df = df.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]
    
    if fuel_types:
        filtered_df = filtered_df[filtered_df['descCarburante'].isin(fuel_types)]
    
    if regions:
        filtered_df = filtered_df[filtered_df['Regione'].isin(regions)]
        group_cols = ['Periodo', 'Regione', 'descCarburante']
    else:
        group_cols = ['Periodo', 'descCarburante']
    
    if agg_level == 'daily':
        filtered_df['Periodo'] = filtered_df['Data']
    elif agg_level == 'weekly':
        filtered_df['Periodo'] = filtered_df['Data'].dt.to_period('W').dt.start_time
    elif agg_level == 'monthly':
        filtered_df['Periodo'] = filtered_df['Data'].dt.to_period('M').dt.to_timestamp()
    else: # yearly
        filtered_df['Periodo'] = filtered_df['Data'].dt.to_period('Y').dt.to_timestamp()
        
    if filtered_df.empty:
        cols = group_cols + ['prezzo']
        return pd.DataFrame(columns=cols)

    ts_data = filtered_df.groupby(group_cols)['prezzo'].mean().reset_index()
    
    if not regions:
        ts_data['Regione'] = 'Italy Average'
    
    return ts_data

def get_kpi_data(df, fuel_type, start_date=None, end_date=None, month=None, year=None):
    """
    Calculates average price for a fuel type in a given period or specific month.
    """
    filtered_df = df.copy()
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]
    elif month and year:
        filtered_df = filtered_df[(filtered_df['year'] == year) & (filtered_df['month'] == month)]
    
    filtered_df = filtered_df[filtered_df['descCarburante'] == fuel_type]
    
    if filtered_df.empty:
        return 0.0
    
    return filtered_df['prezzo'].mean()
