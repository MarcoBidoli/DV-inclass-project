import pandas as pd
import os
import config

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
    
    # Parse dates
    df['Data'] = pd.to_datetime(df['Data'])
    df['year'] = df['Data'].dt.year
    df['month'] = df['Data'].dt.month
    
    # Apply mapping
    df['REG_MAPPED'] = df['Regione'].map(lambda x: REGION_MAPPING.get(x, x))
    
    # Remove outliers or invalid prices if any
    df = df[df['prezzo'] > 0]

    if config.DEBUG:
        print("------DEBUG START------")
        print(df.head(3))
        print("------DEBUG END------")
    
    return df
