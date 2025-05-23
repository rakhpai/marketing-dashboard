"""
BigQuery metadata queries for dashboard overview.
"""

from ..config.settings import settings

class MetadataQueries:
    """Collection of queries to get metadata about the data"""
    
    @staticmethod
    def get_data_overview(domain: str = None) -> str:
        """Get overview of data in BigQuery"""
        return f"""
        WITH data_stats AS (
            SELECT 
                COUNT(*) as total_rows,
                MIN(date) as earliest_date,
                MAX(date) as latest_date,
                COUNT(DISTINCT DATE(date)) as days_with_data,
                COUNT(DISTINCT query) as unique_queries,
                COUNT(DISTINCT url) as unique_pages,
                COUNT(DISTINCT country) as unique_countries,
                SUM(clicks) as total_clicks,
                SUM(impressions) as total_impressions
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            WHERE url IS NOT NULL
        ),
        last_update AS (
            SELECT 
                MAX(date) as last_data_date,
                CURRENT_TIMESTAMP() as current_time,
                DATE_DIFF(CURRENT_DATE(), DATE(MAX(date)), DAY) as days_since_update
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        )
        SELECT 
            ds.*,
            lu.last_data_date,
            lu.current_time,
            lu.days_since_update
        FROM data_stats ds
        CROSS JOIN last_update lu
        """
    
    @staticmethod
    def get_data_freshness() -> str:
        """Check data freshness across different tables"""
        return f"""
        WITH table_stats AS (
            SELECT 
                'search_console_data' as table_name,
                COUNT(*) as row_count,
                MAX(date) as latest_date,
                MIN(date) as earliest_date
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
            
            UNION ALL
            
            SELECT 
                'keyword_tracking' as table_name,
                COUNT(*) as row_count,
                MAX(created_at) as latest_date,
                MIN(created_at) as earliest_date
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.keyword_tracking`
        )
        SELECT 
            table_name,
            row_count,
            latest_date,
            earliest_date,
            DATE_DIFF(CURRENT_DATE(), DATE(latest_date), DAY) as days_since_update,
            DATE_DIFF(DATE(latest_date), DATE(earliest_date), DAY) + 1 as days_of_data
        FROM table_stats
        ORDER BY table_name
        """
    
    @staticmethod
    def get_daily_data_volume(days_back: int = 30, domain: str = None) -> str:
        """Get daily data volume for monitoring"""
        return f"""
        SELECT 
            DATE(date) as date,
            COUNT(*) as row_count,
            COUNT(DISTINCT query) as unique_queries,
            COUNT(DISTINCT url) as unique_pages,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        GROUP BY DATE(date)
        ORDER BY date ASC
        """
    
    @staticmethod
    def get_data_quality_check(domain: str = None) -> str:
        """Check data quality metrics"""
        return f"""
        WITH quality_metrics AS (
            SELECT 
                COUNT(*) as total_rows,
                COUNT(CASE WHEN query IS NULL OR query = '' THEN 1 END) as null_queries,
                COUNT(CASE WHEN url IS NULL OR url = '' THEN 1 END) as null_pages,
                COUNT(CASE WHEN clicks > impressions THEN 1 END) as invalid_clicks,
                COUNT(CASE WHEN ctr > 1 THEN 1 END) as invalid_ctr,
                COUNT(CASE WHEN position < 0 OR position > 1000 THEN 1 END) as invalid_position
            FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.search_console_data`
        )
        SELECT 
            total_rows,
            null_queries,
            ROUND(null_queries * 100.0 / NULLIF(total_rows, 0), 2) as null_queries_pct,
            null_pages,
            ROUND(null_pages * 100.0 / NULLIF(total_rows, 0), 2) as null_pages_pct,
            invalid_clicks,
            ROUND(invalid_clicks * 100.0 / NULLIF(total_rows, 0), 2) as invalid_clicks_pct,
            invalid_ctr,
            ROUND(invalid_ctr * 100.0 / NULLIF(total_rows, 0), 2) as invalid_ctr_pct,
            invalid_position,
            ROUND(invalid_position * 100.0 / NULLIF(total_rows, 0), 2) as invalid_position_pct
        FROM quality_metrics
        """
    
    @staticmethod
    def get_table_schema(table_name: str) -> str:
        """Get schema information for a specific table"""
        return f"""
        SELECT 
            column_name,
            data_type,
            is_nullable,
            is_partitioned,
            clustering_ordinal_position
        FROM `{settings.bigquery_project_id}.{settings.bigquery_dataset}.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
        """