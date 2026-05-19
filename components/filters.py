from dash import dcc, html
import dash_bootstrap_components as dbc

def create_theme_switch():
    """
    Creates a simple theme switch for Dark Mode.
    """
    return html.Div([
        dbc.Checklist(
            options=[{"label": "Dark Mode", "value": 1}],
            value=[],
            id="theme-switch",
            switch=True,
            className="ms-auto"
        )
    ], className="d-flex")

def create_map_controls(month_options):
    """
    Creates the fuel toggle switch and 100% width monthly slider without numeric tooltip.
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
                        marks={},
                        updatemode='drag'
                    )
                ], width=12),
            ])
        ])
    ], className="mb-4 shadow-sm border-0")
