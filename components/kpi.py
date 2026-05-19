from dash import html
import dash_bootstrap_components as dbc

def create_kpi_card(title, value, color):
    """
    Creates a simple KPI card with digital font for value.
    """
    return dbc.Card([
        dbc.CardBody([
            html.H5(title, className="card-title text-muted mb-1", style={'fontSize': '1.0rem'}), # ~0.9 * 1.1
            html.H2([
                html.Span("€", style={'fontSize': '1.9rem', 'verticalAlign': 'baseline', 'marginRight': '5px'}), # ~1.75 * 1.1
                f"{value:.3f}"
            ], className="kpi-value mb-0", 
               style={'color': color, 'fontWeight': 'bold', 'fontFamily': 'DS-Digital', 'fontSize': '3.85rem', 'display': 'flex', 'alignItems': 'baseline'}) # 3.5 * 1.1
        ])
    ], className="shadow-sm border-0 mb-3")

def create_kpi_section(petrol_price, diesel_price):
    """
    Creates the KPI section with two cards.
    """
    return dbc.Row([
        dbc.Col([
            create_kpi_card("Average Petrol Price", petrol_price, "#006400") # Dark Green
        ], md=6),
        dbc.Col([
            create_kpi_card("Average Diesel Price", diesel_price, "#FBC02D") # Dark Yellow
        ], md=6)
    ])
