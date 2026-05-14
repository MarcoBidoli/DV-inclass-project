import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import json

# Region mapping to match GeoJSON
region_mapping = {
    'Trentino-Alto Adige': 'Trentino-Alto Adige/Südtirol',
    'Friuli Venezia Giulia': 'Friuli-Venezia Giulia',
    'Valle d\'Aosta': 'Valle d\'Aosta/Vallée d\'Aoste'
}

def load_data():
    try:
        summary_df = pd.read_csv('summary_data.csv')
        dist_df = pd.read_csv('distribution_data.csv')
        with open('limits_IT_regions.geojson', 'r') as f:
            geojson = json.load(f)
        
        # Apply mapping
        summary_df['DEN_REG_MAPPED'] = summary_df['DEN_REG'].replace(region_mapping)
        dist_df['DEN_REG_MAPPED'] = dist_df['DEN_REG'].replace(region_mapping)
        
        return summary_df, dist_df, geojson
    except FileNotFoundError:
        return None, None, None

summary_df, dist_df, geojson = load_data()

if summary_df is not None:
    # Create list of months for the slider
    summary_df['date_month'] = pd.to_datetime(summary_df[['year', 'month']].assign(day=1))
    all_months = sorted(summary_df['date_month'].unique())
    month_options = {i: date.strftime('%b %Y') for i, date in enumerate(all_months)}
    
    fuel_types = sorted(summary_df['descCarburante'].unique())
    regions = sorted(summary_df['DEN_REG'].unique())
    years = sorted(summary_df['year'].unique())
else:
    all_months = []
    month_options = {}
    fuel_types = []
    regions = []
    years = []

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("🇮🇹 Italy Fuel Price Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                html.Label("⛽ Fuel Type", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='fuel-filter', options=[{'label': f, 'value': f} for f in fuel_types], value='Benzina', clearable=False)
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
            
            html.Div([
                html.Label("📍 Highlight Region", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='region-filter', options=[{'label': 'All Regions', 'value': 'All'}] + [{'label': r, 'value': r} for r in regions], value='All')
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
            
            html.Div([
                html.Label("📅 Year Filter", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='year-filter', options=[{'label': 'All Years', 'value': 'All'}] + [{'label': str(y), 'value': y} for y in years], value='All')
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 10px'}),
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                html.Label("🕒 Select Month-Year", style={'fontWeight': 'bold', 'marginRight': '20px'}),
                html.Button("▶️ Play", id="play-button", n_clicks=0, style={'marginRight': '10px', 'padding': '5px 15px', 'borderRadius': '5px', 'border': '1px solid #ccc', 'cursor': 'pointer'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            dcc.Slider(
                id='month-slider',
                min=0,
                max=len(all_months) - 1,
                value=len(all_months) - 1,
                marks={i: {'label': date.strftime('%m/%y'), 'style': {'fontSize': '10px'}} for i, date in enumerate(all_months) if i % 6 == 0},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Interval(id='play-interval', interval=1000, n_intervals=0, disabled=True)
        ], style={'padding': '20px', 'marginBottom': '30px'}),
        
        html.Div([
            html.Div([
                dcc.Graph(id='choropleth-map', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(id='bar-chart', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),
        
        html.Div([
            dcc.Graph(id='price-dist', config={'displayModeBar': False})
        ], style={'width': '100%'})
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'})
])

# Play/Pause Logic
@app.callback(
    [Output('play-interval', 'disabled'),
     Output('play-button', 'children')],
    [Input('play-button', 'n_clicks')],
    [dash.State('play-interval', 'disabled')]
)
def toggle_play(n_clicks, disabled):
    if n_clicks == 0:
        return True, "▶️ Play"
    if disabled:
        return False, "⏸️ Pause"
    else:
        return True, "▶️ Play"

# Advance Slider
@app.callback(
    Output('month-slider', 'value', allow_duplicate=True),
    Input('play-interval', 'n_intervals'),
    [dash.State('month-slider', 'value'),
     dash.State('month-slider', 'max')],
    prevent_initial_call=True
)
def advance_slider(n_intervals, current_val, max_val):
    if current_val >= max_val:
        return 0
    return current_val + 1

# Synchronize Year Filter and Slider
@app.callback(
    Output('month-slider', 'value'),
    Input('year-filter', 'value'),
    prevent_initial_call=True
)
def sync_slider(year):
    if year == 'All':
        return len(all_months) - 1
    for i, date in enumerate(all_months):
        if date.year == year:
            return i
    return dash.no_update

@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('price-dist', 'figure')],
    [Input('fuel-filter', 'value'),
     Input('region-filter', 'value'),
     Input('month-slider', 'value')]
)
def update_plots(fuel_type, region, month_idx):
    if summary_df is None:
        return {}, {}, {}
    
    selected_date = all_months[month_idx]
    
    # Filter for Map and Bar
    map_df = summary_df[
        (summary_df['date_month'] == selected_date) & 
        (summary_df['descCarburante'] == fuel_type)
    ].copy()
    
    # Filter for Distribution
    d_df = dist_df[
        (dist_df['year'] == selected_date.year) & 
        (dist_df['month'] == selected_date.month) &
        (dist_df['descCarburante'] == fuel_type)
    ]
    
    if region != 'All':
        d_df = d_df[d_df['DEN_REG'] == region]

    # Map Figure
    fig_map = px.choropleth_mapbox(
        map_df,
        geojson=geojson,
        locations='DEN_REG_MAPPED',
        featureidkey='properties.reg_name',
        color='mean_prezzo',
        color_continuous_scale="RdYlGn_r",
        mapbox_style="carto-positron",
        zoom=4.5,
        center={"lat": 42.0, "lon": 12.5},
        opacity=0.8,
        labels={'mean_prezzo': 'Avg Price (€)'},
        title=f"<b>Price Heatmap</b>"
    )
    fig_map.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        title_x=0.5,
        coloraxis_colorbar=dict(title="€/L")
    )

    # Bar Chart (Race)
    # Sort for the race effect
    bar_df = map_df.sort_values('mean_prezzo', ascending=True)
    
    # Apply color highlighting to selected region
    colors = ['#3498db'] * len(bar_df)
    if region != 'All':
        if region in bar_df['DEN_REG'].values:
            idx = bar_df[bar_df['DEN_REG'] == region].index[0]
            # Since we sorted, we need to find the new index
            pos = bar_df.index.get_loc(idx)
            colors[pos] = '#e74c3c' # Red for selected

    fig_bar = px.bar(
        bar_df,
        x='mean_prezzo',
        y='DEN_REG',
        orientation='h',
        title=f"<b>Regional Ranking</b>",
        labels={'mean_prezzo': 'Avg Price (€)', 'DEN_REG': 'Region'},
        text_auto='.3f'
    )
    fig_bar.update_traces(marker_color=colors)
    fig_bar.update_layout(
        margin={"r":20,"t":40,"l":0,"b":40},
        title_x=0.5,
        xaxis=dict(range=[bar_df['mean_prezzo'].min()*0.95, bar_df['mean_prezzo'].max()*1.05]),
        yaxis=dict(autorange="reversed") # Highest on top
    )

    # Distribution Figure
    fig_dist = px.histogram(
        d_df,
        x='prezzo',
        nbins=30,
        title=f"<b>Price Distribution - {selected_date.strftime('%B %Y')}</b>",
        labels={'prezzo': 'Price (€)'},
        color_discrete_sequence=['#2ecc71']
    )
    fig_dist.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#eee'),
        yaxis=dict(gridcolor='#eee'),
        margin={"t":60}
    )
    
    return fig_map, fig_bar, fig_dist

if __name__ == '__main__':
    app.run(debug=True, port=8050)
