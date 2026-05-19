import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import json
import os
import pandas as pd
from datetime import datetime

# Import custom utilities and components
import config
from utils.preprocessing import load_and_clean_data
from utils.aggregations import get_regional_summary, get_time_series, get_kpi_data
from utils.caching import setup_cache
from components.maps import create_choropleth_map, create_deviation_map
from components.barchart import create_bar_chart
from components.linechart import create_line_chart
from components.filters import create_map_controls, create_theme_switch
from components.kpi import create_kpi_section

# 1. Initialize App
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&display=swap",
        "https://fonts.cdnfonts.com/css/ds-digital"
    ],
    suppress_callback_exceptions=True
)

# 2. Setup Data and Cache
cache = setup_cache(app)
data_path = os.path.join(os.path.dirname(__file__), 'data', 'filtered_fuel_prices_italy_20200101-20260518.csv')
full_df = load_and_clean_data(data_path)
geojson_path = os.path.join(os.path.dirname(__file__), 'data', 'italy_regions.geojson')
with open(geojson_path, 'r') as f:
    geojson = json.load(f)

regions = sorted(full_df['Regione'].unique())
month_df = full_df[['year', 'month']].drop_duplicates().sort_values(['year', 'month'])
month_options = [
    {'label': f"{row['month']}/{row['year']}", 
     'year': row['year'], 'month': row['month']} 
    for _, row in month_df.iterrows()
]

# 3. Define Layout
app.layout = html.Div([
    # Header
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Italy Fuel Price Dashboard", className="fw-bold mb-0"),
                    html.P([
                        "Regional analytics and historical trends. Source: ",
                        html.A("Ministero delle Imprese e del Made in Italy (MIMIT)", 
                               href="https://www.mimit.gov.it/it/open-data/elenco-dataset/carburanti-prezzi-praticati-e-anagrafica-degli-impianti",
                               target="_blank",
                               className="text-decoration-none")
                    ], className="lead text-muted mb-0")
                ], md=9),
                dbc.Col([
                    create_theme_switch()
                ], md=3, className="d-flex align-items-center justify-content-end")
            ])
        ], fluid=True)
    ], className="dashboard-header py-4 shadow-sm mb-4"),

    dbc.Container([
        # Global Controls: KPI
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div(id='kpi-container')
                ], width=12)
            ])
        ], className="mb-4"),
        
        # Maps Section
        html.Div([
            create_map_controls(month_options),
            
            html.Div([
                html.Div("Regional Fuel Prices", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='choropleth-map', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container p-4 shadow-sm mb-4 border-0 rounded"),
            
            html.Div([
                html.Div("Regional Deviation from National Average", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='deviation-map', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container p-4 shadow-sm mb-4 border-0 rounded"),
        ]),
        
        # Ranking Section
        html.Div([
            html.Div([
                html.Div("Regional Fuel Price Ranking", className="h4 mb-3 fw-bold"),
                dcc.Graph(id='bar-chart', config={'displayModeBar': False}, style={'height': '700px'})
            ], className="card-container p-4 shadow-sm mb-4 border-0 rounded"),
        ]),

        # Line Chart Section
        html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div("Fuel Price Evolution Over Time", className="h4 mb-0 fw-bold"),
                    ], md=6),
                    dbc.Col([
                        dbc.RadioItems(
                            id="time-granularity",
                            options=[
                                {"label": "Daily", "value": "daily"},
                                {"label": "Weekly", "value": "weekly"},
                                {"label": "Monthly", "value": "monthly"},
                            ],
                            value="monthly",
                            inline=True,
                            className="d-flex justify-content-end",
                            inputCheckedClassName="bg-primary border-primary",
                            labelStyle={"marginLeft": "1rem", "fontSize": "0.9rem"}
                        )
                    ], md=6, className="d-flex align-items-center")
                ], className="mb-3"),
                dcc.Graph(id='line-chart', config={'displayModeBar': False}, style={'height': '600px'})
            ], className="card-container p-4 shadow-sm mb-4 border-0 rounded"),
        ])

    ], className="main-container pb-5", fluid=True)
], id="main-wrapper", style={'backgroundColor': 'var(--bg-light)', 'minHeight': '100vh'})

# 4. Callbacks

# Theme Switcher Logic
app.clientside_callback(
    dash.ClientsideFunction(
        namespace='clientside',
        function_name='toggle_theme'
    ),
    Output('main-wrapper', 'className'),
    Input('theme-switch', 'value')
)

# Maps, KPIs, Ranking and Line Chart
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('deviation-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('kpi-container', 'children'),
     Output('line-chart', 'figure')],
    [Input('map-fuel-toggle', 'value'),
     Input('month-slider', 'value'),
     Input('theme-switch', 'value'),
     Input('time-granularity', 'value')]
)
def update_all_visuals(fuel_toggle, month_idx, theme_value, granularity):
    # fuel_toggle is a list: [1] if checked (Gasolio), [] if unchecked (Benzina)
    fuel_type = 'Gasolio' if fuel_toggle and 1 in fuel_toggle else 'Benzina'
    selected_month = month_options[month_idx]
    m = selected_month['month']
    y = selected_month['year']
    label = selected_month['label']

    # Theme color
    text_color = '#f0f6fc' if (theme_value and len(theme_value) > 0) else '#2c3e50'

    # 1. KPIs (Synchronized with selected month)
    benzina_avg = get_kpi_data(full_df, 'Benzina', month=m, year=y)
    gasolio_avg = get_kpi_data(full_df, 'Gasolio', month=m, year=y)
    kpi_section = create_kpi_section(benzina_avg, gasolio_avg)

    # 2. Summary Data for Maps (Filtered by selected fuel type)
    map_summary_df = get_regional_summary(full_df, month=m, year=y, fuel_type=fuel_type)

    # Map Figs
    fig_map = create_choropleth_map(map_summary_df, geojson, fuel_type, label)
    fig_dev = create_deviation_map(map_summary_df, geojson, fuel_type, label)

    # Bar Chart (Now synchronized with the chosen fuel type)
    fig_bar = create_bar_chart(map_summary_df, fuel_type, label)

    # 3. Line Chart (Full History, User-selected Granularity)
    ts_df = get_time_series(full_df, regions=None, fuel_types=['Benzina', 'Gasolio'], agg_level=granularity)
    line_fig = create_line_chart(ts_df)
    
    # Update chart themes and interactivity
    chart_bg = 'rgba(0,0,0,0)'
    is_dark = (theme_value and len(theme_value) > 0)
    grid_color = '#e0e0e0' if not is_dark else '#30363d'
    mapbox_style = "carto-positron" if not is_dark else "carto-darkmatter"
    
    for f in [fig_map, fig_dev, fig_bar, line_fig]:
        f.update_layout(
            paper_bgcolor=chart_bg,
            plot_bgcolor=chart_bg,
            font=dict(color=text_color, family='IBM Plex Sans')
        )
        if hasattr(f, 'layout') and 'mapbox' in f.layout:
            f.update_layout(mapbox_style=mapbox_style)
    
    # Update axes for bar and line charts
    for f in [fig_bar, line_fig]:
        f.update_xaxes(gridcolor=grid_color, zerolinecolor=grid_color)
        f.update_yaxes(gridcolor=grid_color, zerolinecolor=grid_color)

    # Specific line chart hover enhancements and range slider theming
    event_color = "#2c3e50" if not is_dark else "#f0f6fc"
    
    events = [
        {"date": datetime(2022, 2, 24), "text": "Russian invasion of Ukraine", "y": 0.95},
        {"date": datetime(2022, 3, 22), "text": "Italian government excise duty cut", "y": 0.85},
        {"date": datetime(2026, 2, 28), "text": "Attack of Iran from USA", "y": 0.95},
        {"date": datetime(2026, 3, 18), "text": "Italian government excise duty cut", "y": 0.85},
    ]

    for event in events:
        line_fig.add_shape(
            type="line",
            x0=event["date"], x1=event["date"],
            y0=0, y1=1, yref="paper",
            line=dict(color=event_color, width=2, dash="dot")
        )
        line_fig.add_annotation(
            x=event["date"], y=event["y"], yref="paper",
            text=event["text"],
            showarrow=False,
            xanchor="right",
            yanchor="bottom",
            font=dict(size=11, color=event_color)
        )

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
            spikecolor="#999999",
            rangeslider=dict(
                visible=True,
                bgcolor='rgba(0,0,0,0)',
                thickness=0.1,
                bordercolor=grid_color
            )
        )
    )
    
    return fig_map, fig_dev, fig_bar, kpi_section, line_fig

if __name__ == '__main__':
    if config.DEBUG:
        app.run(debug=True, port=8050)
    else:
        app.run(debug=False, port=8050)
