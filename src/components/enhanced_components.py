"""
Enhanced UI components for the marketing dashboard.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Union
import pandas as pd

def load_enhanced_css():
    """Load custom CSS for enhanced styling"""
    st.markdown("""
    <style>
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .metric-delta.positive {
        color: #4ade80;
    }
    
    .metric-delta.negative {
        color: #f87171;
    }
    
    /* Section headers */
    .section-header {
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        color: #1f2937;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #f3f4f6;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    /* Custom button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f9fafb;
    }
    
    /* Charts container */
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def create_enhanced_metric_card(title: str, value: Union[str, int, float], 
                              delta: Optional[Union[str, int, float]] = None, 
                              delta_color: str = "normal",
                              prefix: str = "",
                              suffix: str = "") -> None:
    """Create an enhanced metric card with gradient background"""
    
    # Format the value
    if isinstance(value, (int, float)):
        if value >= 1000000:
            formatted_value = f"{value/1000000:.1f}M"
        elif value >= 1000:
            formatted_value = f"{value/1000:.1f}K"
        else:
            formatted_value = f"{value:,.0f}"
    else:
        formatted_value = str(value)
    
    # Add prefix and suffix
    formatted_value = f"{prefix}{formatted_value}{suffix}"
    
    # Determine delta class
    delta_class = ""
    delta_icon = ""
    if delta is not None:
        if isinstance(delta, (int, float)):
            if delta > 0:
                delta_class = "positive"
                delta_icon = "▲"
            elif delta < 0:
                delta_class = "negative"
                delta_icon = "▼"
            delta_text = f"{abs(delta):.1f}%"
        else:
            delta_text = str(delta)
    else:
        delta_text = ""
    
    # Create the HTML
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{formatted_value}</div>
        {f'<div class="metric-delta {delta_class}">{delta_icon} {delta_text}</div>' if delta is not None else ''}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def create_enhanced_trend_chart(data: pd.DataFrame, title: str, 
                              x_col: str, y_col: str,
                              color: str = '#667eea',
                              show_average: bool = False) -> go.Figure:
    """Create an enhanced trend chart with customization options"""
    
    fig = go.Figure()
    
    # Main line
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color),
        hovertemplate='%{x}<br>%{y:,.0f}<extra></extra>'
    ))
    
    # Add average line if requested
    if show_average and len(data) > 0:
        avg_value = data[y_col].mean()
        fig.add_hline(
            y=avg_value, 
            line_dash="dash", 
            line_color="gray",
            annotation_text=f"Average: {avg_value:,.0f}"
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 20}
        },
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        height=400,
        hovermode='x unified',
        showlegend=False
    )
    
    # Add gradient fill under the line
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        fill='tozeroy',
        fillcolor=f'rgba(102, 126, 234, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    return fig

def create_comparison_chart(data: pd.DataFrame, title: str,
                          categories: List[str], values: List[str],
                          chart_type: str = 'bar') -> go.Figure:
    """Create a comparison chart (bar or radar)"""
    
    if chart_type == 'bar':
        fig = go.Figure()
        
        colors = ['#667eea', '#764ba2', '#a855f7', '#ec4899']
        
        for i, value_col in enumerate(values):
            fig.add_trace(go.Bar(
                name=value_col,
                x=data[categories[0]] if categories else data.index,
                y=data[value_col],
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title=title,
            barmode='group',
            template='plotly_white',
            height=400
        )
        
    elif chart_type == 'radar':
        fig = go.Figure()
        
        for value_col in values:
            fig.add_trace(go.Scatterpolar(
                r=data[value_col],
                theta=data[categories[0]] if categories else data.index,
                fill='toself',
                name=value_col
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, data[values].max().max()]
                )),
            showlegend=True,
            title=title,
            height=400
        )
    
    return fig

def create_donut_chart(labels: List[str], values: List[Union[int, float]], 
                      title: str, hole_size: float = 0.4) -> go.Figure:
    """Create a donut chart"""
    
    colors = ['#667eea', '#764ba2', '#a855f7', '#ec4899', '#f59e0b', '#10b981']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole_size,
        marker=dict(colors=colors[:len(labels)]),
        textposition='inside',
        textinfo='percent+label'
    )])
    
    fig.update_layout(
        title=title,
        showlegend=True,
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_heatmap(data: pd.DataFrame, title: str,
                  x_labels: Optional[List[str]] = None,
                  y_labels: Optional[List[str]] = None) -> go.Figure:
    """Create a heatmap visualization"""
    
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=x_labels or data.columns,
        y=y_labels or data.index,
        colorscale='Viridis',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_loading_spinner():
    """Create a loading spinner"""
    st.markdown("""
    <div class="loading-spinner">
        <div class="spinner-border text-primary" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_info_box(title: str, content: str, icon: str = "ℹ️"):
    """Create an information box"""
    st.markdown(f"""
    <div class="info-box">
        <strong>{icon} {title}</strong><br>
        {content}
    </div>
    """, unsafe_allow_html=True)

def create_section_header(title: str):
    """Create a styled section header"""
    st.markdown(f'<h2 class="section-header">{title}</h2>', unsafe_allow_html=True)

def create_multi_metric_row(metrics: List[Dict[str, Any]]):
    """Create a row of multiple metric cards"""
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            create_enhanced_metric_card(
                title=metric.get('title', ''),
                value=metric.get('value', 0),
                delta=metric.get('delta'),
                delta_color=metric.get('delta_color', 'normal'),
                prefix=metric.get('prefix', ''),
                suffix=metric.get('suffix', '')
            )