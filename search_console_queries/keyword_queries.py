"""
Keyword specific queries for Search Console data.
"""

from .base_queries import SearchConsoleQueries
import pandas as pd
import logging

# Set up logging
logger = logging.getLogger(__name__)

class KeywordQueries:
    """Queries for keyword analysis from Search Console data"""
    
    def __init__(self, credentials_path=None):
        """Initialize with base query client"""
        self.base_client = SearchConsoleQueries(credentials_path)
        
    def get_top_keywords(self, days_back=30, limit=100, domain=None):
        """
        Get top keywords by clicks
        
        Args:
            days_back (int): Number of days to look back
            limit (int): Maximum number of keywords to return
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with top keywords
        """
        logger.info(f"Getting top {limit} keywords for last {days_back} days")
        
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        query = f"""
        SELECT 
            query,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL AND query != ''
            {domain_filter}
        GROUP BY
            query
        ORDER BY
            total_clicks DESC
        LIMIT {limit}
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error getting top keywords: {e}")
            return pd.DataFrame()
            
    def get_keyword_trend(self, keyword, days_back=90, domain=None):
        """
        Get trend data for a specific keyword
        
        Args:
            keyword (str): Keyword to analyze
            days_back (int): Number of days to look back
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with daily metrics for the keyword
        """
        logger.info(f"Getting trend for keyword '{keyword}' for last {days_back} days")
        
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        query = f"""
        SELECT 
            DATE(date) AS date,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query = '{keyword}'
            {domain_filter}
        GROUP BY
            date
        ORDER BY
            date ASC
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error getting keyword trend: {e}")
            return pd.DataFrame()
            
    def get_keywords_by_position_range(self, min_position, max_position, days_back=30, limit=100, domain=None):
        """
        Get keywords within a specific position range
        
        Args:
            min_position (float): Minimum position (inclusive)
            max_position (float): Maximum position (inclusive)
            days_back (int): Number of days to look back
            limit (int): Maximum number of keywords to return
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with keywords in the position range
        """
        logger.info(f"Getting keywords in position range {min_position}-{max_position} for last {days_back} days")
        
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        query = f"""
        SELECT 
            query,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL AND query != ''
            {domain_filter}
        GROUP BY
            query
        HAVING
            average_position >= {min_position} AND average_position <= {max_position}
        ORDER BY
            total_clicks DESC
        LIMIT {limit}
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error getting keywords by position range: {e}")
            return pd.DataFrame()
