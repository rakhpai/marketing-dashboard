#!/usr/bin/env python3
"""
Run Search Console queries and display results.
"""

import argparse
import pandas as pd
import os
import sys
import logging
from datetime import datetime

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_console_queries import (
    TimePeriodQueries,
    DomainQueries,
    KeywordQueries,
    PageQueries
)
from search_console_queries.utils import format_metrics, save_to_csv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run Search Console queries')
    
    parser.add_argument('--credentials', type=str, help='Path to Google Cloud credentials file')
    parser.add_argument('--domain', type=str, help='Domain to filter by')
    parser.add_argument('--output-dir', type=str, default='./output', help='Output directory for CSV files')
    
    # Query type arguments
    parser.add_argument('--time-period', action='store_true', help='Run time period queries')
    parser.add_argument('--domains', action='store_true', help='Run domain queries')
    parser.add_argument('--keywords', action='store_true', help='Run keyword queries')
    parser.add_argument('--pages', action='store_true', help='Run page queries')
    
    # Time period options
    parser.add_argument('--days', type=int, choices=[7, 30, 90], default=30, help='Number of days to look back')
    
    # Keyword options
    parser.add_argument('--keyword', type=str, help='Specific keyword to analyze')
    parser.add_argument('--limit', type=int, default=100, help='Maximum number of results to return')
    
    # Page options
    parser.add_argument('--page-url', type=str, help='Specific page URL to analyze')
    
    return parser.parse_args()

def run_time_period_queries(args):
    """Run time period queries"""
    logger.info("Running time period queries")
    
    client = TimePeriodQueries(args.credentials)
    
    if args.days == 7:
        df = client.get_last_7_days_metrics(args.domain)
    elif args.days == 90:
        df = client.get_last_90_days_metrics(args.domain)
    else:
        df = client.get_last_30_days_metrics(args.domain)
        
    if df.empty:
        logger.warning("No data found for time period query")
        return
        
    print("\n=== Time Period Metrics ===")
    print(f"Period: Last {args.days} days")
    if args.domain:
        print(f"Domain: {args.domain}")
        
    formatted_df = format_metrics(df)
    print(formatted_df)
    
    # Save to CSV
    save_to_csv(df, f"time_period_{args.days}_days", args.output_dir)
    
    # Get daily metrics
    daily_df = client.get_daily_metrics_for_period(args.days, args.domain)
    
    if not daily_df.empty:
        print("\n=== Daily Metrics ===")
        print(daily_df.head())
        
        # Save to CSV
        save_to_csv(daily_df, f"daily_metrics_{args.days}_days", args.output_dir)

def run_domain_queries(args):
    """Run domain queries"""
    logger.info("Running domain queries")
    
    client = DomainQueries(args.credentials)
    
    # Get available domains
    domains = client.get_available_domains()
    
    if not domains:
        logger.warning("No domains found")
        return
        
    print("\n=== Available Domains ===")
    for i, domain in enumerate(domains, 1):
        print(f"{i}. {domain}")
        
    # If a specific domain is provided, get metrics for that domain
    if args.domain:
        # Get domain comparison with the specified domain and the first few other domains
        comparison_domains = [args.domain]
        for domain in domains:
            if domain != args.domain and len(comparison_domains) < 3:
                comparison_domains.append(domain)
                
        df = client.get_domain_comparison(comparison_domains, args.days)
        
        if not df.empty:
            print("\n=== Domain Comparison ===")
            print(df.head())
            
            # Save to CSV
            save_to_csv(df, f"domain_comparison_{args.days}_days", args.output_dir)

def run_keyword_queries(args):
    """Run keyword queries"""
    logger.info("Running keyword queries")
    
    client = KeywordQueries(args.credentials)
    
    # Get top keywords
    df = client.get_top_keywords(args.days, args.limit, args.domain)
    
    if df.empty:
        logger.warning("No data found for keyword query")
        return
        
    print("\n=== Top Keywords ===")
    print(f"Period: Last {args.days} days")
    if args.domain:
        print(f"Domain: {args.domain}")
        
    formatted_df = format_metrics(df)
    print(formatted_df.head(10))  # Show top 10
    
    # Save to CSV
    save_to_csv(df, f"top_keywords_{args.days}_days", args.output_dir)
    
    # If a specific keyword is provided, get trend for that keyword
    if args.keyword:
        trend_df = client.get_keyword_trend(args.keyword, args.days, args.domain)
        
        if not trend_df.empty:
            print(f"\n=== Keyword Trend: {args.keyword} ===")
            print(trend_df.head())
            
            # Save to CSV
            save_to_csv(trend_df, f"keyword_trend_{args.keyword}_{args.days}_days", args.output_dir)

def run_page_queries(args):
    """Run page queries"""
    logger.info("Running page queries")
    
    client = PageQueries(args.credentials)
    
    # Get top pages
    df = client.get_top_pages(args.days, args.limit, args.domain)
    
    if df.empty:
        logger.warning("No data found for page query")
        return
        
    print("\n=== Top Pages ===")
    print(f"Period: Last {args.days} days")
    if args.domain:
        print(f"Domain: {args.domain}")
        
    formatted_df = format_metrics(df)
    print(formatted_df.head(10))  # Show top 10
    
    # Save to CSV
    save_to_csv(df, f"top_pages_{args.days}_days", args.output_dir)
    
    # If a specific page URL is provided, get trend for that page
    if args.page_url:
        trend_df = client.get_page_trend(args.page_url, args.days)
        
        if not trend_df.empty:
            print(f"\n=== Page Trend: {args.page_url} ===")
            print(trend_df.head())
            
            # Save to CSV
            save_to_csv(trend_df, f"page_trend_{args.days}_days", args.output_dir)
            
        # Get keywords for the page
        keywords_df = client.get_page_keywords(args.page_url, args.days, args.limit)
        
        if not keywords_df.empty:
            print(f"\n=== Keywords for Page: {args.page_url} ===")
            print(keywords_df.head(10))  # Show top 10
            
            # Save to CSV
            save_to_csv(keywords_df, f"page_keywords_{args.days}_days", args.output_dir)

def main():
    """Main function"""
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Run queries based on arguments
    if args.time_period:
        run_time_period_queries(args)
        
    if args.domains:
        run_domain_queries(args)
        
    if args.keywords:
        run_keyword_queries(args)
        
    if args.pages:
        run_page_queries(args)
        
    # If no specific query type is specified, run all
    if not (args.time_period or args.domains or args.keywords or args.pages):
        run_time_period_queries(args)
        run_domain_queries(args)
        run_keyword_queries(args)
        run_page_queries(args)

if __name__ == '__main__':
    main()
