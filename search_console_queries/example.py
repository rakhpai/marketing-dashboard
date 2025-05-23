#!/usr/bin/env python3
"""
Example usage of the Search Console Queries package.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_console_queries import (
    TimePeriodQueries,
    KeywordQueries,
    PageQueries
)
from search_console_queries.utils import format_metrics, plot_daily_metrics

def main():
    """Main function"""
    print("Search Console Queries Example")
    print("=============================")
    
    # Initialize clients
    time_period_client = TimePeriodQueries()
    keyword_client = KeywordQueries()
    page_client = PageQueries()
    
    # Get metrics for different time periods
    print("\n1. Getting metrics for different time periods...")
    
    metrics_7d = time_period_client.get_last_7_days_metrics()
    metrics_30d = time_period_client.get_last_30_days_metrics()
    metrics_90d = time_period_client.get_last_90_days_metrics()
    
    print("\nLast 7 Days Metrics:")
    print(format_metrics(metrics_7d))
    
    print("\nLast 30 Days Metrics:")
    print(format_metrics(metrics_30d))
    
    print("\nLast 90 Days Metrics:")
    print(format_metrics(metrics_90d))
    
    # Get daily metrics for the last 30 days
    print("\n2. Getting daily metrics for the last 30 days...")
    
    daily_metrics = time_period_client.get_daily_metrics_for_period(30)
    
    print("\nDaily Metrics (first 5 rows):")
    print(daily_metrics.head())
    
    # Plot daily metrics
    if not daily_metrics.empty:
        print("\nPlotting daily metrics...")
        fig = plot_daily_metrics(
            daily_metrics,
            metric_cols=['total_clicks', 'total_impressions'],
            title="Daily Clicks and Impressions (Last 30 Days)"
        )
        plt.show()
    
    # Get top keywords
    print("\n3. Getting top keywords for the last 30 days...")
    
    top_keywords = keyword_client.get_top_keywords(days_back=30, limit=10)
    
    print("\nTop Keywords (first 10):")
    print(format_metrics(top_keywords))
    
    # Get top pages
    print("\n4. Getting top pages for the last 30 days...")
    
    top_pages = page_client.get_top_pages(days_back=30, limit=10)
    
    print("\nTop Pages (first 10):")
    print(format_metrics(top_pages))
    
    print("\nExample completed!")

if __name__ == '__main__':
    main()
