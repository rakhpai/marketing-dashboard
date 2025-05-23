#!/usr/bin/env python3
"""
Verify Daily Data Volume metrics by querying BigQuery directly.
This script checks the last 60 days of search_console_data.
"""

import os
import sys
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration
CREDENTIALS_PATH = "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/credentials/seo-integration-key.json"
PROJECT_ID = "gtm-management-twelvetransfers"
DATASET_ID = "seo_data"
TABLE_ID = "search_console_data"

def verify_daily_data_volume():
    """Query BigQuery to verify daily data volume metrics"""
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ Credentials file not found at: {CREDENTIALS_PATH}")
        # Try alternative path
        alt_path = "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json"
        if os.path.exists(alt_path):
            print(f"✅ Found credentials at alternative path: {alt_path}")
            credentials_path = alt_path
        else:
            print("❌ No credentials file found!")
            return
    else:
        credentials_path = CREDENTIALS_PATH
    
    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        
        # Create BigQuery client
        client = bigquery.Client(
            credentials=credentials,
            project=PROJECT_ID
        )
        
        print(f"✅ Connected to BigQuery project: {PROJECT_ID}")
        print(f"📊 Querying dataset: {DATASET_ID}")
        print("-" * 60)
        
        # Query for daily data volume (last 60 days)
        query = f"""
        SELECT 
            DATE(date) as date,
            COUNT(*) as row_count,
            COUNT(DISTINCT query) as unique_queries,
            COUNT(DISTINCT url) as unique_pages,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
        GROUP BY DATE(date)
        ORDER BY date ASC
        """
        
        print("🔍 Running query for daily data volume (last 60 days)...")
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list for processing
        rows = list(results)
        
        if not rows:
            print("❌ No data found in the specified date range!")
            return
        
        # Calculate summary statistics
        days_with_data = len(rows)
        total_clicks = sum(row.total_clicks for row in rows if row.total_clicks)
        total_impressions = sum(row.total_impressions for row in rows if row.total_impressions)
        total_unique_queries = sum(row.unique_queries for row in rows if row.unique_queries)
        avg_daily_clicks = total_clicks / days_with_data if days_with_data > 0 else 0
        
        print("\n📈 DAILY DATA VOLUME SUMMARY (Last 60 Days)")
        print("=" * 60)
        print(f"Days with Data: {days_with_data}")
        print(f"Total Clicks: {total_clicks:,}")
        print(f"Average Daily Clicks: {avg_daily_clicks:.1f}")
        print(f"Total Unique Queries: {total_unique_queries:,}")
        print(f"Total Impressions: {total_impressions:,}")
        print("=" * 60)
        
        print("\n🗓️ COMPARISON WITH DASHBOARD VALUES")
        print("-" * 60)
        print("Dashboard shows:")
        print("  - Days with Data: 4")
        print("  - Total Clicks: 580")
        print("  - Avg Daily Clicks: 145.0")
        print("  - Total Queries: 3,939")
        print("\nActual values:")
        print(f"  - Days with Data: {days_with_data}")
        print(f"  - Total Clicks: {total_clicks:,}")
        print(f"  - Avg Daily Clicks: {avg_daily_clicks:.1f}")
        print(f"  - Total Queries: {total_unique_queries:,}")
        
        # Show daily breakdown for the days with data
        print("\n📅 DAILY BREAKDOWN (Days with data only)")
        print("-" * 60)
        print(f"{'Date':<12} {'Clicks':<10} {'Impressions':<12} {'Queries':<10} {'Pages':<10}")
        print("-" * 60)
        
        for row in rows:
            if row.total_clicks > 0:  # Only show days with actual data
                print(f"{row.date.strftime('%Y-%m-%d'):<12} "
                      f"{row.total_clicks:<10,} "
                      f"{row.total_impressions:<12,} "
                      f"{row.unique_queries:<10,} "
                      f"{row.unique_pages:<10,}")
        
        # Additional query to check the most recent data
        recent_query = f"""
        SELECT 
            MAX(date) as latest_date,
            MIN(date) as earliest_date,
            COUNT(DISTINCT DATE(date)) as total_days_with_data
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
        """
        
        print("\n🕒 DATA FRESHNESS CHECK")
        print("-" * 60)
        recent_job = client.query(recent_query)
        recent_results = recent_job.result()
        
        for row in recent_results:
            print(f"Latest data: {row.latest_date}")
            print(f"Earliest data (last 60 days): {row.earliest_date}")
            print(f"Total days with data: {row.total_days_with_data}")
            days_since_update = (datetime.now().date() - row.latest_date).days
            print(f"Days since last update: {days_since_update}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_daily_data_volume()