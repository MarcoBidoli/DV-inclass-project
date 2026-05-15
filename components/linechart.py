import plotly.express as px

def create_line_chart(df, agg_level='monthly'):
    """
    Creates the time series line chart.
    """
    if df.empty:
        return px.line(title="No data available")
    
    x_col = 'Data' if 'Data' in df.columns else 'Periodo'
    
    fig = px.line(
        df,
        x=x_col,
        y='prezzo',
        color='Regione',
        line_group='Regione',
        hover_name='Regione',
        title=f"<b>Price Evolution ({agg_level.capitalize()})</b>",
        labels={'prezzo': 'Price (€/L)', x_col: 'Date', 'Regione': 'Region'},
        color_discrete_map={'National Average': '#dc3545'}
    )
    
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(title="Price (€/L)"),
        margin={"t":60, "l":0, "r":20, "b":0},
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        transition_duration=500
    )
    
    return fig
