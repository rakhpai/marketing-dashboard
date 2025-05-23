"""
Data access layer for marketing dashboard.
"""

from typing import Optional, Dict, Any, List
import pandas as pd
import logging
from datetime import datetime, timedelta

from .bigquery_client import MarketingBigQueryClient
from .supabase_client import MarketingSupabaseClient
from .queries import MarketingQueries
from .metadata_queries import MetadataQueries
from .view_queries import ViewQueries
from .simple_queries import SimpleQueries
from ..config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

# Initialize clients
_bigquery_client = None
_supabase_client = None

def get_bigquery_client() -> MarketingBigQueryClient:
    """Get or create BigQuery client singleton"""
    global _bigquery_client
    if _bigquery_client is None:
        _bigquery_client = MarketingBigQueryClient()
    return _bigquery_client

def get_supabase_client() -> MarketingSupabaseClient:
    """Get or create Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = MarketingSupabaseClient()
    return _supabase_client

# Data fetching functions
def get_search_performance_data(start_date: str, end_date: str, domain: Optional[str] = None) -> pd.DataFrame:
    """Get search console performance data"""
    try:
        client = get_bigquery_client()
        # Use simple query for now
        query = SimpleQueries.get_search_performance_simple(start_date, end_date)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching search performance data: {e}")
        return pd.DataFrame()

def get_keyword_data(limit: int = 100, days_back: int = 30, domain: Optional[str] = None) -> pd.DataFrame:
    """Get top performing keywords"""
    try:
        client = get_bigquery_client()
        # Use simple query for now
        query = SimpleQueries.get_keyword_performance_simple(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching keyword data: {e}")
        return pd.DataFrame()

def get_page_performance_data(limit: int = 50, days_back: int = 30, domain: Optional[str] = None) -> pd.DataFrame:
    """Get top performing pages"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_page_performance(limit, days_back, domain)
        else:
            query = MarketingQueries.get_page_performance(limit, days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching page performance data: {e}")
        return pd.DataFrame()

def get_traffic_by_device(start_date: str, end_date: str, domain: Optional[str] = None) -> pd.DataFrame:
    """Get traffic breakdown by device"""
    try:
        client = get_bigquery_client()
        # Simplified query without domain filter
        query = f"""
        SELECT 
            device,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) BETWEEN '{start_date}' AND '{end_date}'
            AND device IS NOT NULL
        GROUP BY device
        ORDER BY total_clicks DESC
        """
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching device traffic data: {e}")
        return pd.DataFrame()

def get_traffic_by_country(start_date: str, end_date: str, limit: int = 20, domain: Optional[str] = None) -> pd.DataFrame:
    """Get traffic breakdown by country"""
    try:
        client = get_bigquery_client()
        # Simplified query without domain filter
        query = f"""
        SELECT 
            country,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) BETWEEN '{start_date}' AND '{end_date}'
            AND country IS NOT NULL
        GROUP BY country
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching country traffic data: {e}")
        return pd.DataFrame()

def get_keyword_trends(keyword: str, days_back: int = 90, domain: Optional[str] = None) -> pd.DataFrame:
    """Get trend data for a specific keyword"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_keyword_trends(keyword, days_back, domain)
        else:
            query = MarketingQueries.get_keyword_trends(keyword, days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching keyword trends: {e}")
        return pd.DataFrame()

def get_competitor_analysis(days_back: int = 30) -> pd.DataFrame:
    """Get competitor position analysis"""
    try:
        client = get_bigquery_client()
        query = MarketingQueries.get_competitor_analysis(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching competitor analysis: {e}")
        return pd.DataFrame()

def get_conversion_funnel_data(start_date: str, end_date: str, domain: Optional[str] = None) -> Dict[str, int]:
    """Get conversion funnel data"""
    try:
        client = get_bigquery_client()
        # Simplified query without domain filter
        query = f"""
        WITH funnel_data AS (
            SELECT 
                SUM(impressions) as impressions,
                SUM(clicks) as clicks
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            WHERE DATE(date) BETWEEN '{start_date}' AND '{end_date}'
        )
        SELECT 
            impressions,
            clicks,
            CAST(clicks * 0.15 AS INT64) as estimated_bookings,
            CAST(clicks * 0.15 * 0.8 AS INT64) as estimated_conversions
        FROM funnel_data
        """
        df = client.query_to_dataframe(query)
        
        if not df.empty:
            row = df.iloc[0]
            return {
                "Impressions": int(row.get('impressions', 0)),
                "Clicks": int(row.get('clicks', 0)),
                "Bookings": int(row.get('estimated_bookings', 0)),
                "Conversions": int(row.get('estimated_conversions', 0))
            }
        return {"Impressions": 0, "Clicks": 0, "Bookings": 0, "Conversions": 0}
    except Exception as e:
        logger.error(f"Error fetching conversion funnel data: {e}")
        return {"Impressions": 0, "Clicks": 0, "Bookings": 0, "Conversions": 0}

def get_weekly_performance_summary(domain: Optional[str] = None) -> pd.DataFrame:
    """Get weekly performance summary"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_weekly_performance_summary(domain)
        else:
            query = MarketingQueries.get_weekly_performance_summary()
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching weekly summary: {e}")
        return pd.DataFrame()

def get_monthly_performance_summary(domain: Optional[str] = None) -> pd.DataFrame:
    """Get monthly performance summary"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_monthly_performance_summary(domain)
        else:
            query = MarketingQueries.get_monthly_performance_summary()
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching monthly summary: {e}")
        return pd.DataFrame()

def get_landing_page_performance(days_back: int = 30, domain: Optional[str] = None) -> pd.DataFrame:
    """Get landing page performance metrics"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_landing_page_performance(days_back, domain)
        else:
            query = MarketingQueries.get_landing_page_performance(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching landing page performance: {e}")
        return pd.DataFrame()

def get_query_category_performance(days_back: int = 30, domain: Optional[str] = None) -> pd.DataFrame:
    """Get performance by query categories"""
    try:
        client = get_bigquery_client()
        # Simplified query for branded vs non-branded
        query = f"""
        SELECT 
            CASE 
                WHEN LOWER(query) LIKE '%twelve%' OR LOWER(query) LIKE '%12%transfers%' THEN 'Branded'
                ELSE 'Non-Branded'
            END as query_type,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT query) as unique_queries
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL
        GROUP BY query_type
        ORDER BY total_clicks DESC
        """
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching query category performance: {e}")
        return pd.DataFrame()

def get_top_opportunities(min_impressions: int = 1000, max_position: float = 20, domain: Optional[str] = None) -> pd.DataFrame:
    """Get keywords with high impressions but low CTR"""
    try:
        client = get_bigquery_client()
        if domain:
            query = MarketingQueries.get_top_opportunities(min_impressions, max_position, domain)
        else:
            query = MarketingQueries.get_top_opportunities(min_impressions, max_position)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching top opportunities: {e}")
        return pd.DataFrame()

# Metadata functions
def get_data_overview(domain: Optional[str] = 'twelvetransfers.com') -> Dict[str, Any]:
    """Get overview of data in BigQuery"""
    try:
        client = get_bigquery_client()
        query = MetadataQueries.get_data_overview(domain)
        df = client.query_to_dataframe(query)
        
        if not df.empty:
            row = df.iloc[0]
            return {
                "total_rows": int(row.get('total_rows', 0)),
                "earliest_date": row.get('earliest_date'),
                "latest_date": row.get('latest_date'),
                "days_with_data": int(row.get('days_with_data', 0)),
                "unique_queries": int(row.get('unique_queries', 0)),
                "unique_pages": int(row.get('unique_pages', 0)),
                "unique_countries": int(row.get('unique_countries', 0)),
                "total_clicks": int(row.get('total_clicks', 0)),
                "total_impressions": int(row.get('total_impressions', 0)),
                "last_data_date": row.get('last_data_date'),
                "current_time": row.get('current_time'),
                "days_since_update": int(row.get('days_since_update', 0))
            }
        return {}
    except Exception as e:
        logger.error(f"Error fetching data overview: {e}")
        return {}

def get_data_freshness() -> pd.DataFrame:
    """Check data freshness across different tables"""
    try:
        client = get_bigquery_client()
        query = MetadataQueries.get_data_freshness()
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching data freshness: {e}")
        return pd.DataFrame()

def get_daily_data_volume(days_back: int = 30, domain: Optional[str] = 'twelvetransfers.com') -> pd.DataFrame:
    """Get daily data volume for monitoring"""
    try:
        client = get_bigquery_client()
        query = MetadataQueries.get_daily_data_volume(days_back, domain)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching daily data volume: {e}")
        return pd.DataFrame()

def get_data_quality_check(domain: Optional[str] = 'twelvetransfers.com') -> Dict[str, Any]:
    """Check data quality metrics"""
    try:
        client = get_bigquery_client()
        query = MetadataQueries.get_data_quality_check(domain)
        df = client.query_to_dataframe(query)
        
        if not df.empty:
            return df.iloc[0].to_dict()
        return {}
    except Exception as e:
        logger.error(f"Error fetching data quality check: {e}")
        return {}

# View-based data functions
def get_search_console_daily_trend(days_back: int = 30) -> pd.DataFrame:
    """Get daily trend from search_console_overview view"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_search_console_daily_trend(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching daily trend: {e}")
        return pd.DataFrame()

def get_top_keywords_from_view(limit: int = 50) -> pd.DataFrame:
    """Get top keywords from keyword_performance view"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_top_keywords_from_view(limit)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching top keywords from view: {e}")
        return pd.DataFrame()

def get_top_pages_from_view(limit: int = 50) -> pd.DataFrame:
    """Get top pages from page_performance view"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_top_pages_from_view(limit)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching top pages from view: {e}")
        return pd.DataFrame()

def get_tracked_keywords_with_positions(limit: int = 100) -> pd.DataFrame:
    """Get tracked keywords with their current positions"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_tracked_keywords_with_positions(limit)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching tracked keywords: {e}")
        return pd.DataFrame()

def get_ga4_event_summary(days_back: int = 7) -> pd.DataFrame:
    """Get GA4 event summary"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_ga4_event_summary(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching GA4 events: {e}")
        return pd.DataFrame()

def get_ga4_daily_users(days_back: int = 7) -> pd.DataFrame:
    """Get daily active users from GA4"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_ga4_daily_users(days_back)
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching GA4 daily users: {e}")
        return pd.DataFrame()

def get_position_distribution() -> pd.DataFrame:
    """Get distribution of keyword positions"""
    try:
        client = get_bigquery_client()
        query = ViewQueries.get_position_distribution()
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error fetching position distribution: {e}")
        return pd.DataFrame()

# Simple data functions
def get_recent_data_check() -> pd.DataFrame:
    """Check what data we have recently"""
    try:
        client = get_bigquery_client()
        query = SimpleQueries.get_recent_data_check()
        return client.query_to_dataframe(query)
    except Exception as e:
        logger.error(f"Error checking recent data: {e}")
        return pd.DataFrame()

# Helper functions
def test_bigquery_connection() -> bool:
    """Test BigQuery connection"""
    try:
        client = get_bigquery_client()
        return client.test_connection()
    except Exception as e:
        logger.error(f"Error testing BigQuery connection: {e}")
        return False

def test_supabase_connection() -> bool:
    """Test Supabase connection"""
    try:
        client = get_supabase_client()
        return client.test_connection()
    except Exception as e:
        logger.error(f"Error testing Supabase connection: {e}")
        return False