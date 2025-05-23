"""
Utility functions for Search Console queries.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

def format_metrics(df):
    """
    Format metrics for display
    
    Args:
        df (pd.DataFrame): DataFrame with metrics
        
    Returns:
        pd.DataFrame: Formatted DataFrame
    """
    if df.empty:
        return df
        
    # Make a copy to avoid modifying the original
    formatted_df = df.copy()
    
    # Format CTR as percentage
    if 'average_ctr' in formatted_df.columns:
        formatted_df['average_ctr'] = formatted_df['average_ctr'].apply(lambda x: f"{x*100:.2f}%" if pd.notnull(x) else "N/A")
        
    # Format position to 1 decimal place
    if 'average_position' in formatted_df.columns:
        formatted_df['average_position'] = formatted_df['average_position'].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A")
        
    return formatted_df

def save_to_csv(df, filename, output_dir='./output'):
    """
    Save DataFrame to CSV
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Filename
        output_dir (str): Output directory
        
    Returns:
        str: Path to saved file
    """
    if df.empty:
        logger.warning(f"DataFrame is empty, not saving {filename}")
        return None
        
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Add timestamp to filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = os.path.join(output_dir, f"{filename}_{timestamp}.csv")
    
    # Save to CSV
    df.to_csv(path, index=False)
    logger.info(f"Saved to {path}")
    
    return path

def plot_daily_metrics(df, metric_cols=None, title=None, figsize=(12, 6), output_file=None):
    """
    Plot daily metrics
    
    Args:
        df (pd.DataFrame): DataFrame with daily metrics
        metric_cols (list): List of metric columns to plot
        title (str): Plot title
        figsize (tuple): Figure size
        output_file (str): Output file path
        
    Returns:
        plt.Figure: Matplotlib figure
    """
    if df.empty:
        logger.warning("DataFrame is empty, not creating plot")
        return None
        
    if 'date' not in df.columns:
        logger.warning("DataFrame does not have a 'date' column, not creating plot")
        return None
        
    # Default metric columns if not specified
    if metric_cols is None:
        metric_cols = ['total_clicks', 'total_impressions']
        
    # Filter to only include columns that exist in the DataFrame
    metric_cols = [col for col in metric_cols if col in df.columns]
    
    if not metric_cols:
        logger.warning("No valid metric columns found, not creating plot")
        return None
        
    # Create plot
    plt.figure(figsize=figsize)
    
    # Set style
    sns.set_style("whitegrid")
    
    # Plot each metric
    for col in metric_cols:
        sns.lineplot(x='date', y=col, data=df, label=col)
        
    # Set title and labels
    plt.title(title or "Daily Metrics")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save if output file is specified
    if output_file:
        plt.savefig(output_file)
        logger.info(f"Saved plot to {output_file}")
        
    return plt.gcf()

def calculate_period_over_period_change(current_df, previous_df, metric_cols=None):
    """
    Calculate period-over-period change
    
    Args:
        current_df (pd.DataFrame): Current period DataFrame
        previous_df (pd.DataFrame): Previous period DataFrame
        metric_cols (list): List of metric columns to compare
        
    Returns:
        pd.DataFrame: DataFrame with period-over-period changes
    """
    if current_df.empty or previous_df.empty:
        logger.warning("One or both DataFrames are empty, not calculating changes")
        return pd.DataFrame()
        
    # Default metric columns if not specified
    if metric_cols is None:
        metric_cols = ['total_clicks', 'total_impressions', 'average_ctr', 'average_position']
        
    # Filter to only include columns that exist in both DataFrames
    metric_cols = [col for col in metric_cols if col in current_df.columns and col in previous_df.columns]
    
    if not metric_cols:
        logger.warning("No valid metric columns found, not calculating changes")
        return pd.DataFrame()
        
    # Create DataFrame for changes
    changes = pd.DataFrame()
    
    # Calculate changes for each metric
    for col in metric_cols:
        current_val = current_df[col].iloc[0] if len(current_df) > 0 else 0
        previous_val = previous_df[col].iloc[0] if len(previous_df) > 0 else 0
        
        if previous_val == 0:
            pct_change = float('inf') if current_val > 0 else 0
        else:
            pct_change = (current_val - previous_val) / previous_val
            
        changes[col] = [current_val]
        changes[f"{col}_prev"] = [previous_val]
        changes[f"{col}_change"] = [current_val - previous_val]
        changes[f"{col}_pct_change"] = [pct_change]
        
    return changes
