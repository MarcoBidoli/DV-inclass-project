import plotly.express as px
import json
import os

def create_choropleth_map(df, geojson, fuel_type, year):
    """
    Creates the absolute price choropleth map.
    """
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='DEN_REG_MAPPED',
        featureidkey='properties.reg_name',
        color='avg_price',
        color_continuous_scale="RdYlGn_r",
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 41.8719, "lon": 12.5674},
        opacity=0.7,
        hover_name='DEN_REG',
        hover_data={
            'DEN_REG_MAPPED': False,
            'avg_price': ':.3f',
            'deviation_abs': ':.3f'
        },
        labels={'avg_price': 'Avg Price (€/L)', 'deviation_abs': 'vs National Avg'},
        title=f"<b>Average {fuel_type} Prices - {year}</b>"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.05,
        clickmode='event+select',
        transition_duration=500,
        coloraxis_colorbar=dict(title="€/L")
    )
    
    return fig

def create_deviation_map(df, geojson, fuel_type, year):
    """
    Creates the deviation map.
    """
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='DEN_REG_MAPPED',
        featureidkey='properties.reg_name',
        color='deviation_pct',
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=0,
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 41.8719, "lon": 12.5674},
        opacity=0.7,
        hover_name='DEN_REG',
        hover_data={
            'DEN_REG_MAPPED': False,
            'avg_price': ':.3f',
            'nat_avg': ':.3f',
            'deviation_pct': ':.2f'
        },
        labels={
            'deviation_pct': 'Deviation (%)',
            'avg_price': 'Region Avg',
            'nat_avg': 'Italy Avg'
        },
        title=f"<b>Deviation from National Average - {year}</b>"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.05,
        clickmode='event+select',
        transition_duration=500,
        coloraxis_colorbar=dict(title="% Diff")
    )
    
    return fig
