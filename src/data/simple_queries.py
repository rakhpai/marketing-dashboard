"""
Simplified BigQuery queries without complex filtering.
"""

from ..config.settings import settings

class SimpleQueries:
    """Simplified queries for testing real data"""
    
    @staticmethod
    def get_search_performance_simple(start_date: str, end_date: str) -> str:
        """Get search console performance - simplified"""
        return f"""
        SELECT 
            DATE(date) as date,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) as avg_ctr,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY DATE(date)
        ORDER BY date DESC
        LIMIT 100
        """
    
    @staticmethod
    def get_keyword_performance_simple(days_back: int = 30) -> str:
        """Get keyword performance - simplified"""
        return f"""
        SELECT 
            query as keyword,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL
            AND query != ''
        GROUP BY query
        HAVING total_clicks > 0
        ORDER BY total_clicks DESC
        LIMIT 50
        """
    
    @staticmethod
    def get_page_performance_simple(days_back: int = 30) -> str:
        """Get page performance - simplified"""
        return f"""
        SELECT 
            url,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions,
            AVG(ctr) * 100 as avg_ctr_percentage,
            AVG(position) as avg_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND url IS NOT NULL
            AND url LIKE '%twelvetransfers%'
        GROUP BY url
        HAVING total_impressions > 10
        ORDER BY total_clicks DESC
        LIMIT 50
        """
    
    @staticmethod
    def get_recent_data_check() -> str:
        """Check what data we have recently"""
        return f"""
        SELECT 
            DATE(date) as date,
            COUNT(*) as row_count,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY DATE(date)
        ORDER BY date DESC
        """