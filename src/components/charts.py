"""
Advanced chart components for marketing analytics.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any, Optional, Union
import numpy as np

def create_conversion_funnel(data: Dict[str, int], title: str = "Marketing Conversion Funnel") -> go.Figure:
    """Create a conversion funnel chart"""
    
    # Extract stages and values
    stages = list(data.keys())
    values = list(data.values())
    
    # Calculate percentages
    initial_value = values[0] if values else 1
    percentages = [(v / initial_value) * 100 for v in values]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        texttemplate="%{label}<br>%{value:,}<br>(%{percentInitial})",
        opacity=0.7,
        marker={
            "color": ["#667eea", "#764ba2", "#a855f7", "#ec4899"],
            "line": {"width": 2, "color": "white"}
        },
        connector={"line": {"color": "#4b5563", "width": 2}}
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 20}
        },
        template='plotly_white',
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_geographic_heatmap(data: pd.DataFrame, 
                            location_col: str,
                            value_col: str,
                            title: str = "Geographic Distribution") -> go.Figure:
    """Create a geographic heatmap"""
    
    fig = px.choropleth(
        data,
        locations=location_col,
        color=value_col,
        hover_name=location_col,
        color_continuous_scale='Viridis',
        title=title,
        labels={value_col: 'Value'}
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_competitor_comparison(data: pd.DataFrame,
                               competitors: List[str],
                               metrics: List[str],
                               title: str = "Competitor Analysis") -> go.Figure:
    """Create a competitor comparison radar chart"""
    
    fig = go.Figure()
    
    # Define colors for each competitor
    colors = ['#667eea', '#764ba2', '#a855f7', '#ec4899', '#f59e0b']
    
    for i, competitor in enumerate(competitors):
        if competitor in data.columns:
            fig.add_trace(go.Scatterpolar(
                r=data[competitor].values,
                theta=metrics,
                fill='toself',
                name=competitor,
                line=dict(color=colors[i % len(colors)], width=2),
                fillcolor=colors[i % len(colors)],
                opacity=0.3
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, data[competitors].max().max() * 1.1]
            )
        ),
        showlegend=True,
        title={
            'text': title,
            'font': {'size': 20}
        },
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_time_series_comparison(data: pd.DataFrame,
                                date_col: str,
                                value_cols: List[str],
                                title: str = "Time Series Comparison") -> go.Figure:
    """Create a time series comparison chart with multiple lines"""
    
    fig = go.Figure()
    
    colors = ['#667eea', '#764ba2', '#a855f7', '#ec4899', '#f59e0b']
    
    for i, col in enumerate(value_cols):
        if col in data.columns:
            fig.add_trace(go.Scatter(
                x=data[date_col],
                y=data[col],
                mode='lines+markers',
                name=col,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6)
            ))
    
    # Add range selector buttons
    fig.update_xaxis(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 20}
        },
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def create_performance_gauge(value: float, 
                           title: str,
                           min_value: float = 0,
                           max_value: float = 100,
                           target: Optional[float] = None) -> go.Figure:
    """Create a performance gauge chart"""
    
    # Define color ranges
    if value >= 80:
        bar_color = "#10b981"  # Green
    elif value >= 60:
        bar_color = "#f59e0b"  # Yellow
    else:
        bar_color = "#ef4444"  # Red
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': target} if target else None,
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': bar_color},
            'steps': [
                {'range': [min_value, max_value * 0.6], 'color': "lightgray"},
                {'range': [max_value * 0.6, max_value * 0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target if target else max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        template='plotly_white',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_traffic_sources_chart(data: pd.DataFrame,
                               source_col: str,
                               value_col: str,
                               title: str = "Traffic Sources") -> go.Figure:
    """Create a sunburst chart for traffic sources"""
    
    # Prepare data for sunburst
    fig = px.sunburst(
        data,
        path=[source_col],
        values=value_col,
        title=title,
        color=value_col,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_keyword_cloud(keywords: pd.DataFrame,
                        keyword_col: str,
                        weight_col: str,
                        title: str = "Keyword Performance") -> go.Figure:
    """Create a treemap as a keyword cloud alternative"""
    
    # Sort and limit to top keywords
    top_keywords = keywords.nlargest(50, weight_col)
    
    fig = px.treemap(
        top_keywords,
        path=[keyword_col],
        values=weight_col,
        title=title,
        color=weight_col,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_cohort_analysis(data: pd.DataFrame,
                         cohort_col: str,
                         period_col: str,
                         value_col: str,
                         title: str = "Cohort Analysis") -> go.Figure:
    """Create a cohort analysis heatmap"""
    
    # Pivot data for heatmap
    cohort_pivot = data.pivot_table(
        index=cohort_col,
        columns=period_col,
        values=value_col,
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=cohort_pivot.values,
        x=cohort_pivot.columns,
        y=cohort_pivot.index,
        colorscale='Blues',
        hoverongaps=False,
        hovertemplate='Cohort: %{y}<br>Period: %{x}<br>Value: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 20}
        },
        xaxis_title=period_col,
        yaxis_title=cohort_col,
        template='plotly_white',
        height=500
    )
    
    return fig

def create_performance_matrix(data: pd.DataFrame,
                            x_col: str,
                            y_col: str,
                            size_col: Optional[str] = None,
                            color_col: Optional[str] = None,
                            title: str = "Performance Matrix") -> go.Figure:
    """Create a scatter plot matrix for performance analysis"""
    
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        size=size_col if size_col else None,
        color=color_col if color_col else None,
        title=title,
        color_continuous_scale='Viridis',
        size_max=50
    )
    
    # Add quadrant lines
    x_mid = data[x_col].median()
    y_mid = data[y_col].median()
    
    fig.add_hline(y=y_mid, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=x_mid, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=data[x_col].min(), y=data[y_col].max(), 
                      text="High Performance<br>Low Effort", showarrow=False)
    fig.add_annotation(x=data[x_col].max(), y=data[y_col].max(), 
                      text="High Performance<br>High Effort", showarrow=False)
    fig.add_annotation(x=data[x_col].min(), y=data[y_col].min(), 
                      text="Low Performance<br>Low Effort", showarrow=False)
    fig.add_annotation(x=data[x_col].max(), y=data[y_col].min(), 
                      text="Low Performance<br>High Effort", showarrow=False)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        height=500
    )
    
    return fig