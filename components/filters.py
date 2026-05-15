from dash import dcc, html
import dash_bootstrap_components as dbc

def create_filters(fuel_types, regions, years):
    """
    Creates the filter UI components.
    """
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Fuel Type"),
                    dcc.Dropdown(
                        id='fuel-filter',
                        options=[{'label': f, 'value': f} for f in fuel_types],
                        value='Benzina',
                        clearable=False
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Aggregation"),
                    dcc.Dropdown(
                        id='agg-filter',
                        options=[
                            {'label': 'Daily', 'value': 'daily'},
                            {'label': 'Monthly', 'value': 'monthly'},
                            {'label': 'Yearly', 'value': 'yearly'}
                        ],
                        value='monthly',
                        clearable=False
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Regions"),
                    dcc.Dropdown(
                        id='region-multi-filter',
                        options=[{'label': r, 'value': r} for r in regions],
                        value=[],
                        multi=True,
                        placeholder="Select regions to compare..."
                    )
                ], md=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("Selected Year"),
                    dcc.Slider(
                        id='year-slider',
                        min=min(years),
                        max=max(years),
                        step=1,
                        value=max(years),
                        marks={str(y): str(y) for y in years},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], md=10),
                dbc.Col([
                    html.Br(),
                    dbc.Button("Play", id="play-btn", color="primary", outline=True, size="sm", className="mt-2 w-100")
                ], md=2)
            ])
        ])
    ], className="shadow-sm mb-4 border-0")
