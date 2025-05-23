"""
Marketing-specific BigQuery queries.
"""

from datetime import datetime, timedelta
from typing import Optional
from ..config.settings import settings

class MarketingQueries:
    """Collection of marketing analytics queries"""
    
    @staticmethod
    def get_search_console_performance(start_date: str, end_date: str, domain: str = 'twelvetransfers.com') -> str:
        """Get search console performance metrics"""
        if domain:
            return f"""
            SELECT 
                date,
                SUM(clicks) as total_clicks,
                SUM(impressions) as total_impressions,
                AVG(ctr) as avg_ctr,
                AVG(position) as avg_position
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
                AND (url LIKE '%{domain}%' OR page LIKE '%{domain}%')
            GROUP BY date
            ORDER BY date DESC
            """
        else:
            return f"""
            SELECT 
                date,
                SUM(clicks) as total_clicks,
                SUM(impressions) as total_impressions,
                AVG(ctr) as avg_ctr,
                AVG(position) as avg_position
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY date
            ORDER BY date DESC
            """
    
    @staticmethod
    def get_keyword_performance(limit: int = 100, days_back: int = 30, domain: str = 'twelvetransfers.com') -> str:
        """Get top performing keywords"""
        return f"""
        SELECT 
            query as keyword,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT date) as days_visible
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL
            AND query != ''
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY query
        HAVING total_clicks > 0
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_page_performance(limit: int = 50, days_back: int = 30, domain: str = 'twelvetransfers.com') -> str:
        """Get top performing pages"""
        return f"""
        SELECT 
            page,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND page IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY page
        HAVING total_impressions > 100
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_traffic_by_device(start_date: str, end_date: str, domain: str = 'twelvetransfers.com') -> str:
        """Get traffic breakdown by device type"""
        return f"""
        SELECT 
            device,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND device IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY device
        ORDER BY total_clicks DESC
        """
    
    @staticmethod
    def get_traffic_by_country(start_date: str, end_date: str, limit: int = 20, domain: str = 'twelvetransfers.com') -> str:
        """Get traffic breakdown by country"""
        return f"""
        SELECT 
            country,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
            AND country IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY country
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_keyword_trends(keyword: str, days_back: int = 90, domain: str = 'twelvetransfers.com') -> str:
        """Get trend data for a specific keyword"""
        return f"""
        SELECT 
            date,
            clicks,
            impressions,
            ctr * 100 as ctr_percentage,
            position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND LOWER(query) = LOWER('{keyword}')
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        ORDER BY date DESC
        """
    
    @staticmethod
    def get_competitor_analysis(days_back: int = 30) -> str:
        """Get competitor position analysis"""
        return f"""
        SELECT 
            company_name,
            keyword,
            AVG(position) as avg_position,
            COUNT(DISTINCT date) as days_tracked,
            MIN(position) as best_position,
            MAX(position) as worst_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_positions`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND position IS NOT NULL
            AND position > 0
        GROUP BY company_name, keyword
        ORDER BY company_name, avg_position
        """
    
    @staticmethod
    def get_conversion_funnel_data(start_date: str, end_date: str, domain: str = 'twelvetransfers.com') -> str:
        """Get conversion funnel data"""
        return f"""
        WITH funnel_data AS (
            SELECT 
                SUM(impressions) as impressions,
                SUM(clicks) as clicks
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
                AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        )
        SELECT 
            impressions,
            clicks,
            CAST(clicks * 0.15 AS INT64) as estimated_bookings,
            CAST(clicks * 0.15 * 0.8 AS INT64) as estimated_conversions
        FROM funnel_data
        """
    
    @staticmethod
    def get_weekly_performance_summary(domain: str = 'twelvetransfers.com') -> str:
        """Get weekly performance summary"""
        return f"""
        SELECT 
            DATE_TRUNC(date, WEEK) as week_start,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT query) as unique_keywords
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 WEEK)
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY week_start
        ORDER BY week_start DESC
        """
    
    @staticmethod
    def get_monthly_performance_summary(domain: str = 'twelvetransfers.com') -> str:
        """Get monthly performance summary"""
        return f"""
        SELECT 
            DATE_TRUNC(date, MONTH) as month_start,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT query) as unique_keywords,
            COUNT(DISTINCT page) as unique_pages
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY month_start
        ORDER BY month_start DESC
        """
    
    @staticmethod
    def get_landing_page_performance(days_back: int = 30, domain: str = 'twelvetransfers.com') -> str:
        """Get landing page performance metrics"""
        return f"""
        SELECT 
            REGEXP_EXTRACT(page, r'^https?://[^/]+(/[^?]*)')  as clean_path,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT query) as unique_keywords
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND page IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY clean_path
        HAVING total_impressions > 100
        ORDER BY total_clicks DESC
        LIMIT 50
        """
    
    @staticmethod
    def get_query_category_performance(days_back: int = 30, domain: str = 'twelvetransfers.com') -> str:
        """Get performance by query categories (branded vs non-branded)"""
        return f"""
        SELECT 
            CASE 
                WHEN LOWER(query) LIKE '%twelve%' OR LOWER(query) LIKE '%12%' THEN 'Branded'
                ELSE 'Non-Branded'
            END as query_type,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            COUNT(DISTINCT query) as unique_queries
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY query_type
        ORDER BY total_clicks DESC
        """
    
    @staticmethod
    def get_top_opportunities(min_impressions: int = 1000, max_position: float = 20, domain: str = 'twelvetransfers.com') -> str:
        """Get keywords with high impressions but low CTR (opportunities)"""
        return f"""
        SELECT 
            query as keyword,
            SUM(impressions) as total_impressions,
            SUM(clicks) as total_clicks,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position,
            SUM(impressions) * (0.3 - AVG(ctr)) as opportunity_score
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            AND query IS NOT NULL
            AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
        GROUP BY query
        HAVING total_impressions >= {min_impressions}
            AND avg_position <= {max_position}
            AND avg_ctr_percentage < 3.0
        ORDER BY opportunity_score DESC
        LIMIT 50
        """