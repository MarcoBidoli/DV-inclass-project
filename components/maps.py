import plotly.express as px
import json
import os

def create_choropleth_map(df, geojson, fuel_type, month_label):
    """
    Creates the absolute price choropleth map.
    """
    # Define colorscale based on fuel type
    # Benzina -> Greens, Gasolio -> Oranges
    color_scale = "Greens" if fuel_type == "Benzina" else "Oranges"
    
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='REG_MAPPED',
        featureidkey='properties.reg_name',
        color='avg_price',
        color_continuous_scale=color_scale,
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 41.8719, "lon": 12.5674},
        opacity=0.7,
        hover_name='Regione',
        hover_data={
            'REG_MAPPED': False,
            'avg_price': ':.3f',
            'nat_avg': ':.3f'
        },
        labels={'avg_price': 'Avg Price (€/L)', 'nat_avg': 'Italy Avg'},
        title=f"<b>{fuel_type} ({month_label})</b>"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.05,
        transition_duration=500,
        coloraxis_colorbar=dict(title="€/L")
    )
    
    return fig

def create_deviation_map(df, geojson, fuel_type, month_label):
    """
    Creates the deviation map.
    Using a diverging scale but customized for the fuel colors if possible.
    Since diverging needs two ends, we'll use a standard diverging scale but ensure titles/labels match.
    """
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='REG_MAPPED',
        featureidkey='properties.reg_name',
        color='deviation_pct',
        color_continuous_scale="RdBu_r", # Red is higher (worse), Blue is lower (better)
        color_continuous_midpoint=0,
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 41.8719, "lon": 12.5674},
        opacity=0.7,
        hover_name='Regione',
        hover_data={
            'REG_MAPPED': False,
            'avg_price': ':.3f',
            'nat_avg': ':.3f',
            'deviation_pct': ':.2f'
        },
        labels={
            'deviation_pct': 'Deviation (%)',
            'avg_price': 'Region Avg',
            'nat_avg': 'Italy Avg'
        },
        title=f"<b>{fuel_type} ({month_label})</b>"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.05,
        transition_duration=500,
        coloraxis_colorbar=dict(title="% Diff")
    )
    
    return fig
