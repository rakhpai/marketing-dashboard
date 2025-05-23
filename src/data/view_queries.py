"""
Queries for BigQuery views.
"""

from ..config.settings import settings

class ViewQueries:
    """Collection of queries using BigQuery views"""
    
    @staticmethod
    def get_search_console_daily_trend(days_back: int = 30) -> str:
        """Get daily trend from search_console_overview view"""
        return f"""
        SELECT 
            date,
            total_clicks,
            total_impressions,
            avg_ctr * 100 as ctr_percentage,
            avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_overview`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        ORDER BY date DESC
        """
    
    @staticmethod
    def get_top_keywords_from_view(limit: int = 50) -> str:
        """Get top keywords from keyword_performance view"""
        return f"""
        SELECT 
            query as keyword,
            total_clicks,
            total_impressions,
            avg_ctr * 100 as ctr_percentage,
            avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_performance`
        WHERE total_clicks > 0
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_top_pages_from_view(limit: int = 50) -> str:
        """Get top pages from page_performance view"""
        return f"""
        SELECT 
            url,
            total_clicks,
            total_impressions,
            avg_ctr * 100 as ctr_percentage,
            avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.page_performance`
        WHERE total_clicks > 0
            AND url LIKE '%twelvetransfers.com%'
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_device_breakdown() -> str:
        """Get device performance from device_performance view"""
        return f"""
        SELECT 
            device,
            total_clicks,
            total_impressions,
            avg_ctr * 100 as ctr_percentage,
            avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.device_performance`
        ORDER BY total_clicks DESC
        """
    
    @staticmethod
    def get_country_breakdown(limit: int = 20) -> str:
        """Get country performance from country_performance view"""
        return f"""
        SELECT 
            country,
            total_clicks,
            total_impressions,
            avg_ctr * 100 as ctr_percentage,
            avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.country_performance`
        WHERE total_clicks > 10
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_keyword_tracking_overview() -> str:
        """Get overview of tracked keywords"""
        return f"""
        SELECT 
            COUNT(DISTINCT keyword) as total_keywords,
            COUNT(DISTINCT search_engine) as search_engines,
            MIN(created_at) as tracking_started,
            MAX(last_checked) as last_update
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_tracking`
        """
    
    @staticmethod
    def get_tracked_keywords_with_positions(limit: int = 100) -> str:
        """Get tracked keywords with their current positions"""
        return f"""
        WITH latest_positions AS (
            SELECT 
                kt.keyword,
                kt.search_engine,
                kt.last_checked,
                org.position,
                org.link,
                org.title,
                ROW_NUMBER() OVER (PARTITION BY kt.keyword ORDER BY org.date_checked DESC, org.position ASC) as rn
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_tracking` kt
            LEFT JOIN `{settings.bigquery_project_id}.{settings.bigquery_dataset}.organic_results` org
                ON kt.id = org.keyword_id
            WHERE org.link LIKE '%twelvetransfers.com%'
        )
        SELECT 
            keyword,
            search_engine,
            position,
            link,
            title,
            last_checked
        FROM latest_positions
        WHERE rn = 1
            AND position IS NOT NULL
        ORDER BY position ASC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_ga4_event_summary(days_back: int = 7) -> str:
        """Get GA4 event summary"""
        return f"""
        SELECT 
            event_name,
            COUNT(*) as event_count,
            COUNT(DISTINCT user_pseudo_id) as unique_users
        FROM `{settings.bigquery_project_id}.analytics_399277695.events_*`
        WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY))
        GROUP BY event_name
        ORDER BY event_count DESC
        LIMIT 20
        """
    
    @staticmethod
    def get_ga4_daily_users(days_back: int = 7) -> str:
        """Get daily active users from GA4"""
        return f"""
        SELECT 
            PARSE_DATE('%Y%m%d', event_date) as date,
            COUNT(DISTINCT user_pseudo_id) as unique_users,
            COUNT(*) as total_events
        FROM `{settings.bigquery_project_id}.analytics_399277695.events_*`
        WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY))
        GROUP BY event_date
        ORDER BY date DESC
        """
    
    @staticmethod
    def get_position_distribution() -> str:
        """Get distribution of keyword positions"""
        return f"""
        WITH current_positions AS (
            SELECT 
                kt.keyword,
                MIN(org.position) as best_position
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_tracking` kt
            JOIN `{settings.bigquery_project_id}.{settings.bigquery_dataset}.organic_results` org
                ON kt.id = org.keyword_id
            WHERE org.link LIKE '%twelvetransfers.com%'
                AND org.position IS NOT NULL
                AND org.position > 0
            GROUP BY kt.keyword
        )
        SELECT 
            CASE 
                WHEN best_position <= 3 THEN 'Top 3'
                WHEN best_position <= 10 THEN 'Top 10'
                WHEN best_position <= 20 THEN 'Top 20'
                WHEN best_position <= 50 THEN 'Top 50'
                ELSE 'Beyond 50'
            END as position_range,
            COUNT(*) as keyword_count
        FROM current_positions
        GROUP BY position_range
        ORDER BY 
            CASE position_range
                WHEN 'Top 3' THEN 1
                WHEN 'Top 10' THEN 2
                WHEN 'Top 20' THEN 3
                WHEN 'Top 50' THEN 4
                ELSE 5
            END
        """