import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import json

# Import custom utilities and components
import config
from utils.preprocessing import load_and_clean_data
from utils.aggregations import get_regional_summary, get_time_series
from utils.caching import setup_cache
from components.maps import create_choropleth_map, create_deviation_map
from components.barchart import create_bar_chart
from components.linechart import create_line_chart
from components.filters import create_filters

# 1. Initialize App
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap"],
    external_scripts=["https://d3js.org/d3.v7.min.js"],
    suppress_callback_exceptions=True,
    title="Italy Fuel Analytics"
)

cache = setup_cache(app)

# 2. Load Data
DATA_PATH = 'data/filtered_fuel_prices_italy_20200101-20260331.csv'
GEOJSON_PATH = 'data/italy_regions.geojson'

full_df = load_and_clean_data(DATA_PATH)
with open(GEOJSON_PATH, 'r') as f:
    geojson = json.load(f)

# Get filter options
fuel_types = sorted(full_df['descCarburante'].unique())
regions = sorted(full_df['Regione'].unique())
years = sorted(full_df['year'].unique())

# 3. Define Layout
app.layout = html.Div([
    # Header
    html.Div([
        dbc.Container([
            html.H1("Italy Fuel Price Dashboard"),
            html.P("Real-time regional analytics and historical trends. Source: Ministero dello Sviluppo Economico.", className="lead text-muted")
        ], fluid=True)
    ], className="dashboard-header py-4 bg-white shadow-sm mb-4"),
    
    # Filters
    dbc.Container([
        html.Div([
            create_filters(fuel_types, regions, years)
        ], className="sticky-top-filters"),
        
        # Main Visuals Row 1: Maps
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Regional Price Heatmap", className="chart-title"),
                    dcc.Graph(id='choropleth-map', config={'displayModeBar': False}, style={'height': '500px'})
                ], className="card-container")
            ], lg=6, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.Div("National Average Deviation", className="chart-title"),
                    dcc.Graph(id='deviation-map', config={'displayModeBar': False}, style={'height': '500px'})
                ], className="card-container")
            ], lg=6, className="mb-4")
        ]),
        
        # Main Visuals Row 2: Ranking & Time Series
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Regional Ranking", className="chart-title"),
                    dcc.Graph(id='bar-chart', config={'displayModeBar': False}, style={'height': '600px'})
                ], className="card-container")
            ], lg=4, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.Div("Fuel Price Evolution", className="chart-title"),
                    dcc.Graph(id='line-chart', config={'displayModeBar': False}, style={'height': '600px'})
                ], className="card-container")
            ], lg=8, className="mb-4")
        ]),
        
        # Hidden Stores for State
        dcc.Store(id='selected-region-store', data=None),
        dcc.Interval(id='play-interval', interval=1500, n_intervals=0, disabled=True)
        
    ], className="main-container", fluid=True)
], style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh'})

# 4. Callbacks

# Play Animation Logic
@app.callback(
    [Output('play-interval', 'disabled'), Output('play-btn', 'children')],
    [Input('play-btn', 'n_clicks')],
    [State('play-interval', 'disabled')]
)
def toggle_play(n_clicks, disabled):
    if n_clicks is None: return True, "Play"
    return not disabled, "Pause" if disabled else "Play"

@app.callback(
    Output('year-slider', 'value'),
    [Input('play-interval', 'n_intervals')],
    [State('year-slider', 'value'), State('year-slider', 'max'), State('year-slider', 'min')]
)
def advance_year(n, current, max_val, min_val):
    if n == 0: return current
    new_year = current + 1
    if new_year > max_val: return min_val
    return new_year

# Regional Selection Interaction
@app.callback(
    Output('selected-region-store', 'data'),
    [Input('choropleth-map', 'clickData'), 
     Input('deviation-map', 'clickData'),
     Input('bar-chart', 'clickData')]
)
def update_region_selection(map_click, dev_click, bar_click):
    ctx = callback_context
    if not ctx.triggered: return None
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'choropleth-map' or trigger_id == 'deviation-map':
        # Map location is MAPPED name
        mapped_name = ctx.triggered[0]['value']['points'][0]['location']
        # Find original region name
        for k, v in REGION_MAPPING.items():
            if v == mapped_name: return k
        return mapped_name
    elif trigger_id == 'bar-chart':
        return ctx.triggered[0]['value']['points'][0]['label']
    
    return None

# Combined Filter & Plot Update
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('deviation-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('line-chart', 'figure')],
    [Input('fuel-filter', 'value'),
     Input('agg-filter', 'value'),
     Input('year-slider', 'value'),
     Input('region-multi-filter', 'value'),
     Input('selected-region-store', 'data')]
)
def update_all_plots(fuel_type, agg_level, year, multi_regions, selected_region):
    # 1. Summary Data (Maps & Bar)
    summary_df = get_regional_summary(full_df, year=year, fuel_type=fuel_type)
    
    # 2. Time Series Data
    ts_regions = multi_regions if multi_regions else []
    if selected_region and selected_region not in ts_regions:
        ts_regions.append(selected_region)
    
    ts_df = get_time_series(full_df, regions=ts_regions, fuel_types=[fuel_type], agg_level=agg_level)
    
    # Generate Figures
    fig_map = create_choropleth_map(summary_df, geojson, fuel_type, year)
    fig_dev = create_deviation_map(summary_df, geojson, fuel_type, year)
    fig_bar = create_bar_chart(summary_df, selected_region=selected_region)
    fig_line = create_line_chart(ts_df, agg_level=agg_level)
    
    return fig_map, fig_dev, fig_bar, fig_line

if __name__ == '__main__':
    from utils.preprocessing import REGION_MAPPING # Ensure mapping is accessible
    if config.DEBUG:
        app.run(debug=True, port=8050)
    else:
        app.run(debug=False, port=8050)