import plotly.express as px

def create_line_chart(df):
    """
    Creates the time series line chart showing multiple fuel types.
    """
    if df.empty:
        return px.line(title="No data available")
    
    x_col = 'Periodo' if 'Periodo' in df.columns else 'Data'
    
    # Sort by period to ensure lines are continuous
    df = df.sort_values(x_col)
    
    fig = px.line(
        df,
        x=x_col,
        y='prezzo',
        color='descCarburante',
        hover_name='descCarburante',
        labels={'prezzo': 'Price (€/L)', x_col: 'Date', 'descCarburante': 'Fuel Type'},
        color_discrete_map={
            'Petrol': '#006400', # Dark Green
            'Diesel': '#FBC02D', # Dark Yellow
        }
    )
    
    # Make lines thicker
    fig.update_traces(line=dict(width=3))
    
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=False),
            type="date"
        ),
        yaxis=dict(title="Price (€/L)"),
        margin={"t":60, "l":40, "r":20, "b":40},
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        transition_duration=500
    )
    
    # Enable interactivity
    fig.update_layout(dragmode='zoom')
    
    return fig
