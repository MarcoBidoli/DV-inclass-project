from dash import dcc, html
import dash_bootstrap_components as dbc

def create_period_filter(min_date, max_date):
    """
    Creates the date range picker for KPIs and Line Chart.
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Select Period"),
            dcc.DatePickerRange(
                id='period-filter',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                display_format='YYYY-MM-DD',
                className="w-100"
            )
        ])
    ], className="mb-4 shadow-sm border-0")

def create_map_controls(month_options):
    """
    Creates the fuel toggle switch (iOS style) and 100% width monthly slider.
    """
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Fuel Type", className="fw-bold mb-2"),
                    html.Div([
                        dbc.Checklist(
                            options=[
                                {"label": "", "value": 1},
                            ],
                            value=[],
                            id="map-fuel-toggle",
                            switch=True,
                            className="ios-switch"
                        ),
                    ], className="d-flex align-items-center mb-2")
                ], md=4, lg=3),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Month", className="fw-bold mb-2"),
                    dcc.Slider(
                        id='month-slider',
                        min=0,
                        max=len(month_options) - 1,
                        step=1,
                        value=len(month_options) - 1,
                        marks={i: month_options[i]['label'] for i in range(0, len(month_options), 4)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], width=12),
            ])
        ])
    ], className="mb-4 shadow-sm border-0")

def create_region_filter(regions):
    """
    Creates the region multi-select filter for the ranking chart.
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Regions"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r} for r in regions],
                value=[],
                multi=True,
                placeholder="Select regions to filter ranking..."
            )
        ])
    ], className="mb-4 shadow-sm border-0")
