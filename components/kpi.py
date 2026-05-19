from dash import html
import dash_bootstrap_components as dbc

def create_kpi_card(title, value, color):
    """
    Creates a simple KPI card with digital font for value.
    """
    return dbc.Card([
        dbc.CardBody([
            html.H5(title, className="card-title text-muted mb-1", style={'fontSize': '0.9rem'}),
            html.H2([
                html.Span("€", style={'fontSize': '1.75rem', 'verticalAlign': 'baseline', 'marginRight': '5px'}),
                f"{value:.3f}"
            ], className="kpi-value mb-0", 
               style={'color': color, 'fontWeight': 'bold', 'fontFamily': 'DS-Digital', 'fontSize': '3.5rem', 'display': 'flex', 'alignItems': 'baseline'})
        ])
    ], className="shadow-sm border-0 mb-3")

def create_kpi_section(benzina_price, gasolio_price):
    """
    Creates the KPI section with two cards.
    """
    return dbc.Row([
        dbc.Col([
            create_kpi_card("Average Benzina Price", benzina_price, "#006400") # Dark Green
        ], md=6),
        dbc.Col([
            create_kpi_card("Average Gasolio Price", gasolio_price, "#E65100") # Dark Orange
        ], md=6)
    ])
