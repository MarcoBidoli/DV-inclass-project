import plotly.express as px
import json
import os


def create_choropleth_map(df, geojson, fuel_type, month_label):
    """
    Creates the absolute price choropleth map
    with visible region borders and no background map.
    """

    # Fuel-dependent colors
    color_scale = "Greens" if fuel_type == "Benzina" else "Oranges"

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations='REG_MAPPED',
        featureidkey='properties.reg_name',
        color='avg_price',
        color_continuous_scale=color_scale,
        projection="mercator",
        hover_name='Regione',
        hover_data={
            'REG_MAPPED': False,
            'avg_price': ':.3f',
            'nat_avg': ':.3f'
        },
        labels={
            'avg_price': 'Avg Price (€/L)',
            'nat_avg': 'Italy Avg'
        },
        title=f"<b>{fuel_type} ({month_label})</b>"
    )

    # Show only Italy polygons and lock view
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    # Add region borders
    fig.update_traces(
        marker_line_width=0.5,
        marker_line_color="gray"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title_x=0.05,
        transition_duration=500,
        coloraxis_colorbar=dict(title="€/L"),
        dragmode=False
    )

    return fig


def create_deviation_map(df, geojson, fuel_type, month_label):
    """
    Creates the deviation percentage map
    with visible region borders and no background map.
    """

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations='REG_MAPPED',
        featureidkey='properties.reg_name',
        color='deviation_pct',
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=0,
        projection="mercator",
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

    # Show only Italy polygons and lock view
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    # Add region borders
    fig.update_traces(
        marker_line_width=0.5,
        marker_line_color="gray"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        title_x=0.05,
        transition_duration=500,
        coloraxis_colorbar=dict(title="% Diff"),
        dragmode=False
    )

    return fig