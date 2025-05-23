"""
Page specific queries for Search Console data.
"""

from .base_queries import SearchConsoleQueries
import pandas as pd
import logging

# Set up logging
logger = logging.getLogger(__name__)

class PageQueries:
    """Queries for page analysis from Search Console data"""
    
    def __init__(self, credentials_path=None):
        """Initialize with base query client"""
        self.base_client = SearchConsoleQueries(credentials_path)
        
    def get_top_pages(self, days_back=30, limit=100, domain=None):
        """
        Get top pages by clicks
        
        Args:
            days_back (int): Number of days to look back
            limit (int): Maximum number of pages to return
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with top pages
        """
        logger.info(f"Getting top {limit} pages for last {days_back} days")
        
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        query = f"""
        SELECT 
            url,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND url IS NOT NULL
            {domain_filter}
        GROUP BY
            url
        ORDER BY
            total_clicks DESC
        LIMIT {limit}
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error getting top pages: {e}")
            return pd.DataFrame()
            
    def get_page_trend(self, page_url, days_back=90, domain=None):
        """
        Get trend data for a specific page
        
        Args:
            page_url (str): Page URL to analyze
            days_back (int): Number of days to look back
            domain (str, optional): Domain to filter by (ignored if page_url is provided)
            
        Returns:
            pd.DataFrame: DataFrame with daily metrics for the page
        """
        logger.info(f"Getting trend for page '{page_url}' for last {days_back} days")
        
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
            AND url = '{page_url}'
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
            logger.error(f"Error getting page trend: {e}")
            return pd.DataFrame()
            
    def get_page_keywords(self, page_url, days_back=30, limit=100):
        """
        Get keywords for a specific page
        
        Args:
            page_url (str): Page URL to analyze
            days_back (int): Number of days to look back
            limit (int): Maximum number of keywords to return
            
        Returns:
            pd.DataFrame: DataFrame with keywords for the page
        """
        logger.info(f"Getting keywords for page '{page_url}' for last {days_back} days")
        
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
            AND url = '{page_url}'
            AND query IS NOT NULL AND query != ''
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
            logger.error(f"Error getting page keywords: {e}")
            return pd.DataFrame()
