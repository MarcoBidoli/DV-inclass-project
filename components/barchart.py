import plotly.graph_objects as go

def create_bar_chart(df, selected_region=None):
    """
    Creates the horizontal bar chart ranking regions.
    """
    if df.empty:
        return go.Figure()
        
    df_sorted = df.sort_values('avg_price', ascending=True)
    
    # Highlight logic
    colors = ['#ced4da'] * len(df_sorted)
    if selected_region:
        for i, reg in enumerate(df_sorted['DEN_REG']):
            if reg == selected_region:
                colors[i] = '#007bff' # Primary blue
                break
    else:
        # Default colors
        colors = ['#adb5bd'] * len(df_sorted)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_sorted['avg_price'],
        y=df_sorted['DEN_REG'],
        orientation='h',
        marker_color=colors,
        text=df_sorted['avg_price'].apply(lambda x: f"{x:.3f}"),
        textposition='auto',
        hovertemplate="<b>%{y}</b><br>Price: €%{x:.3f}/L<extra></extra>"
    ))
    
    # National Average Reference Line
    nat_avg = df['nat_avg'].iloc[0] if not df.empty else 0
    fig.add_vline(x=nat_avg, line_width=2, line_dash="dash", line_color="#dc3545", 
                 annotation_text="Italy Avg", annotation_position="top right")
    
    fig.update_layout(
        title="<b>Regional Price Ranking</b>",
        xaxis=dict(title="Average Price (€/L)", range=[df_sorted['avg_price'].min() * 0.98, df_sorted['avg_price'].max() * 1.02]),
        yaxis=dict(title=""),
        margin={"t":40, "l":0, "r":20, "b":0},
        plot_bgcolor='white',
        transition_duration=500
    )
    
    return fig
