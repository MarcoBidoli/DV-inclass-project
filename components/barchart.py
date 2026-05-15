import plotly.graph_objects as go
import pandas as pd

def create_bar_chart(df, fuel_type, month_label):
    """
    Creates a horizontal bar chart ranking regions for the selected fuel type.
    """
    if df.empty:
        return go.Figure()
        
    # Sort regions by price (highest at top)
    df_sorted = df.sort_values('avg_price', ascending=True)
    
    fuel_colors = {
        'Benzina': '#006400', # Dark Green
        'Gasolio': '#E65100'  # Dark Orange
    }
    
    color = fuel_colors.get(fuel_type, '#6c757d')
    
    fig = go.Figure()
    
    # Trace 1: Region Name (Inside Start, Bold)
    fig.add_trace(go.Bar(
        x=df_sorted['avg_price'],
        y=df_sorted['Regione'],
        name=fuel_type,
        orientation='h',
        marker_color=color,
        text=df_sorted['Regione'],
        textposition='inside',
        insidetextanchor='start',
        textfont=dict(
            color='white',
            size=14,
            family='IBM Plex Sans',
            weight='bold'
        ),
        hovertemplate="<b>%{y}</b><br>Price: €%{x:.3f}/L<extra></extra>"
    ))
    
    # Trace 2: Price (Inside End, Not Bold)
    fig.add_trace(go.Bar(
        x=df_sorted['avg_price'],
        y=df_sorted['Regione'],
        orientation='h',
        marker_color='rgba(0,0,0,0)', # Transparent bar
        text=df_sorted['avg_price'].apply(lambda x: f"€{x:.3f}"),
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(
            color='white',
            size=13,
            family='IBM Plex Sans'
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # National Average Reference Line
    if not df_sorted['nat_avg'].empty:
        nat_avg = df_sorted['nat_avg'].iloc[0]
        if not pd.isna(nat_avg):
            fig.add_vline(
                x=nat_avg, 
                line_width=2, 
                line_dash="dot", 
                line_color=color,
                annotation_text=f"Avg {fuel_type} ({nat_avg:.3f} €/L)", 
                annotation_position="bottom right",
                annotation_font=dict(family='IBM Plex Sans', color=color)
            )
    
    fig.update_layout(
        title=f"<b>Regional {fuel_type} Price Ranking ({month_label})</b>",
        title_font=dict(family='IBM Plex Sans', size=20),
        xaxis=dict(title="Average Price (€/L)", range=[0, df_sorted['avg_price'].max() * 1.15], tickfont=dict(family='IBM Plex Sans')),
        yaxis=dict(title="", showticklabels=False), # Hide standard y-axis labels
        margin={"t":60, "l":0, "r":20, "b":40},
        plot_bgcolor='white',
        height=700,
        barmode='overlay',
        transition_duration=500,
        font=dict(family='IBM Plex Sans')
    )
    
    return fig
