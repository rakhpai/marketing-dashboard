#!/usr/bin/env python3
"""
Verify Daily Data Volume metrics from BigQuery
"""

import os
import sys
sys.path.append('/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing')

from google.cloud import bigquery
from datetime import datetime, timedelta
import json

# Set up credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json'

# Initialize BigQuery client
client = bigquery.Client()

# Query to get daily data volume for last 60 days
query = """
SELECT 
    DATE(date) as date,
    COUNT(*) as row_count,
    COUNT(DISTINCT query) as unique_queries,
    COUNT(DISTINCT url) as unique_pages,
    SUM(clicks) as total_clicks,
    SUM(impressions) as total_impressions
FROM `twelve-transfers-440911.seo_data.search_console_data`
WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
GROUP BY DATE(date)
ORDER BY date ASC
"""

print("Executing query for last 60 days of search console data...")
print("-" * 60)

# Execute query
query_job = client.query(query)
results = list(query_job)

# Calculate metrics
days_with_data = len(results)
total_clicks = sum(row['total_clicks'] for row in results)
total_queries = sum(row['unique_queries'] for row in results)
avg_daily_clicks = total_clicks / days_with_data if days_with_data > 0 else 0

print(f"Days with Data: {days_with_data}")
print(f"Total Clicks: {total_clicks:,}")
print(f"Avg Daily Clicks: {avg_daily_clicks:.1f}")
print(f"Total Queries: {total_queries:,}")
print("-" * 60)

# Show detailed breakdown
print("\nDetailed breakdown by date:")
print("Date\t\tClicks\tImpressions\tQueries\tPages\tRows")
print("-" * 70)

for row in results:
    print(f"{row['date']}\t{row['total_clicks']:,}\t{row['total_impressions']:,}\t\t{row['unique_queries']:,}\t{row['unique_pages']:,}\t{row['row_count']:,}")

# Additional verification - get raw count for comparison
raw_query = """
SELECT 
    COUNT(*) as total_rows,
    SUM(clicks) as total_clicks,
    COUNT(DISTINCT query) as total_unique_queries
FROM `twelve-transfers-440911.seo_data.search_console_data`
WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
"""

print("\n" + "-" * 60)
print("Raw totals for verification:")
raw_job = client.query(raw_query)
raw_results = list(raw_job)[0]

print(f"Total rows in last 60 days: {raw_results['total_rows']:,}")
print(f"Total clicks (raw sum): {raw_results['total_clicks']:,}")
print(f"Total unique queries (distinct count): {raw_results['total_unique_queries']:,}")