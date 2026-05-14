import pandas as pd
import numpy as np
import os

REGION_MAPPING = {
    'Trentino-Alto Adige': 'Trentino-Alto Adige/Südtirol',
    'Friuli Venezia Giulia': 'Friuli-Venezia Giulia',
    'Valle d\'Aosta': 'Valle d\'Aosta/Vallée d\'Aoste',
    'Piemonte': 'Piemonte',
    'Lombardia': 'Lombardia',
    'Veneto': 'Veneto',
    'Liguria': 'Liguria',
    'Emilia-Romagna': 'Emilia-Romagna',
    'Toscana': 'Toscana',
    'Umbria': 'Umbria',
    'Marche': 'Marche',
    'Lazio': 'Lazio',
    'Abruzzo': 'Abruzzo',
    'Molise': 'Molise',
    'Campania': 'Campania',
    'Puglia': 'Puglia',
    'Basilicata': 'Basilicata',
    'Calabria': 'Calabria',
    'Sicilia': 'Sicilia',
    'Sardegna': 'Sardegna'
}

def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    
    # Standardize column names if needed
    if 'Regione' in df.columns:
        df = df.rename(columns={'Regione': 'DEN_REG'})
    
    # Parse dates
    df['Data'] = pd.to_datetime(df['Data'])
    df['year'] = df['Data'].dt.year
    df['month'] = df['Data'].dt.month
    
    # Apply mapping
    df['DEN_REG_MAPPED'] = df['DEN_REG'].map(lambda x: REGION_MAPPING.get(x, x))
    
    # Remove outliers or invalid prices if any
    df = df[df['prezzo'] > 0]
    
    return df
