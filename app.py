import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import json
import pandas as pd

# Import custom utilities and components
import config
from utils.preprocessing import load_and_clean_data
from utils.aggregations import get_regional_summary, get_time_series, get_kpi_data
from utils.caching import setup_cache
from components.maps import create_choropleth_map, create_deviation_map
from components.barchart import create_bar_chart
from components.linechart import create_line_chart
from components.filters import create_period_filter, create_map_controls, create_region_filter
from components.kpi import create_kpi_section

# 1. Initialize App
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True,
    title="Italy Fuel Analytics"
)

cache = setup_cache(app)

# 2. Load Data
DATA_PATH = 'data/filtered_fuel_prices_italy_20200101-20260518.csv'
GEOJSON_PATH = 'data/italy_regions.geojson'

full_df = load_and_clean_data(DATA_PATH)
with open(GEOJSON_PATH, 'r') as f:
    geojson = json.load(f)

# Get filter options
fuel_types = ['Benzina', 'Gasolio'] # Explicitly as per requirements
regions = sorted(full_df['Regione'].unique())
min_date = full_df['Data'].min().date()
max_date = full_df['Data'].max().date()

# Prepare month options for slider
month_df = full_df[['year', 'month']].drop_duplicates().sort_values(['year', 'month'])
month_options = [
    {'label': pd.to_datetime(f"{row['year']}-{row['month']}-01").strftime('%b %Y'), 
     'year': row['year'], 'month': row['month']} 
    for _, row in month_df.iterrows()
]

# 3. Define Layout
app.layout = html.Div([
    # Header
    html.Div([
        dbc.Container([
            html.H1("Italy Fuel Price Dashboard", className="fw-bold"),
            html.P("Regional analytics and historical trends. Source: Ministero dello Sviluppo Economico.", className="lead text-muted")
        ], fluid=True)
    ], className="dashboard-header py-4 bg-white shadow-sm mb-4"),

    dbc.Container([
        # Global Controls: KPI, Period, and Region Filter
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_period_filter(min_date, max_date),
                    create_region_filter(regions)
                ], lg=4),
                dbc.Col([
                    html.Div(id='kpi-container')
                ], lg=8)
            ])
        ], className="mb-4"),
        
        # Maps Section
        html.Div([
            create_map_controls(month_options),
            
            html.Div([
                html.Div("Regional Fuel Prices", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='choropleth-map', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container bg-white p-4 shadow-sm mb-4 border-0 rounded"),
            
            html.Div([
                html.Div("Regional Deviation from National Average", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='deviation-map', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container bg-white p-4 shadow-sm mb-4 border-0 rounded")
        ]),
        
        # Ranking Section
        html.Div([
            html.Div([
                html.Div("Regional Fuel Price Ranking", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='bar-chart', config={'displayModeBar': False}, style={'height': '700px'})
            ], className="card-container bg-white p-4 shadow-sm mb-4 border-0 rounded")
        ]),

        # Line Chart Section
        html.Div([
            html.Div([
                html.Div("Fuel Price Evolution Over Time", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='line-chart', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container bg-white p-4 shadow-sm mb-4 border-0 rounded")
        ])

    ], className="main-container pb-5", fluid=True)
], style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh'})

# 4. Callbacks

# Line Chart (Global Period Filter)
@app.callback(
    Output('line-chart', 'figure'),
    [Input('period-filter', 'start_date'),
     Input('period-filter', 'end_date')]
)
def update_line_chart(start_date, end_date):
    # Line Chart (National Average, Weekly)
    ts_df = get_time_series(full_df, fuel_types=['Benzina', 'Gasolio'], agg_level='weekly', start_date=start_date, end_date=end_date)
    line_fig = create_line_chart(ts_df)
    
    # Enable unified hover with vertical dotted line
    line_fig.update_layout(
        hovermode="x unified",
        spikedistance=-1,
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showline=True,
            showgrid=True,
            spikethickness=1,
            spikedash="dot",
            spikecolor="#999999"
        )
    )
    return line_fig

# Maps, KPIs and Ranking (Monthly Slider and Local Filters)
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('deviation-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('kpi-container', 'children')],
    [Input('map-fuel-toggle', 'value'),
     Input('month-slider', 'value'),
     Input('region-filter', 'value')]
)
def update_monthly_visuals(fuel_toggle, month_idx, filtered_regions):
    # fuel_toggle is a list: [1] if checked (Gasolio), [] if unchecked (Benzina)
    fuel_type = 'Gasolio' if fuel_toggle and 1 in fuel_toggle else 'Benzina'
    selected_month = month_options[month_idx]
    m = selected_month['month']
    y = selected_month['year']
    label = selected_month['label']
    
    # 1. KPIs (Synchronized with selected month)
    benzina_avg = get_kpi_data(full_df, 'Benzina', month=m, year=y)
    gasolio_avg = get_kpi_data(full_df, 'Gasolio', month=m, year=y)
    kpi_section = create_kpi_section(benzina_avg, gasolio_avg)
    
    # 2. Summary Data for Maps (Filtered by selected fuel type)
    map_summary_df = get_regional_summary(full_df, month=m, year=y, fuel_type=fuel_type)
    if filtered_regions:
        map_summary_df = map_summary_df[map_summary_df['Regione'].isin(filtered_regions)]
    
    # Map Figs
    fig_map = create_choropleth_map(map_summary_df, geojson, fuel_type, label)
    fig_dev = create_deviation_map(map_summary_df, geojson, fuel_type, label)
    
    # Bar Chart (Now synchronized with the chosen fuel type)
    fig_bar = create_bar_chart(map_summary_df, fuel_type, label)
    
    return fig_map, fig_dev, fig_bar, kpi_section
if __name__ == '__main__':
    if config.DEBUG:
        app.run(debug=True, port=8050)
    else:
        app.run(debug=False, port=8050)