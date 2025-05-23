"""
Base queries for Search Console data from BigQuery.
"""

from datetime import datetime, timedelta
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
PROJECT_ID = "gtm-management-twelvetransfers"
DATASET_ID = "seo_data"
TABLE_ID = "search_console_data"
OVERVIEW_VIEW_ID = "search_console_overview"

class SearchConsoleQueries:
    """Base class for Search Console queries"""
    
    def __init__(self, credentials_path=None):
        """Initialize with optional credentials path"""
        self.client = None
        self.credentials_path = credentials_path
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize BigQuery client with credentials"""
        try:
            # Try to use provided credentials
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=["https://www.googleapis.com/auth/bigquery"]
                )
                self.client = bigquery.Client(
                    credentials=credentials,
                    project=PROJECT_ID
                )
                logger.info(f"Initialized BigQuery client with provided credentials")
            else:
                # Try to use application default credentials
                self.client = bigquery.Client(project=PROJECT_ID)
                logger.info(f"Initialized BigQuery client with application default credentials")
                
        except Exception as e:
            logger.error(f"Error initializing BigQuery client: {e}")
            raise
            
    def get_search_console_metrics(self, days_back, domain=None):
        """
        Get search console metrics for the specified number of days back
        
        Args:
            days_back (int): Number of days to look back
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with search console metrics
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        query = self._build_metrics_query(start_date, end_date, domain)
        
        try:
            logger.info(f"Executing query for {days_back} days back")
            query_job = self.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()
            
    def _build_metrics_query(self, start_date, end_date, domain=None):
        """
        Build query for search console metrics
        
        Args:
            start_date (date): Start date
            end_date (date): End date
            domain (str, optional): Domain to filter by
            
        Returns:
            str: SQL query
        """
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        return f"""
        SELECT 
            CAST('{start_date}' AS DATE) AS start_date,
            CAST('{end_date}' AS DATE) AS end_date,
            COUNT(DISTINCT DATE(date)) AS days_count,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE 
            DATE(date) BETWEEN '{start_date}' AND '{end_date}'
            {domain_filter}
        """
        
    def get_daily_metrics(self, days_back, domain=None):
        """
        Get daily search console metrics for the specified number of days back
        
        Args:
            days_back (int): Number of days to look back
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with daily search console metrics
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        query = self._build_daily_metrics_query(start_date, end_date, domain)
        
        try:
            logger.info(f"Executing daily metrics query for {days_back} days back")
            query_job = self.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error executing daily metrics query: {e}")
            return pd.DataFrame()
            
    def _build_daily_metrics_query(self, start_date, end_date, domain=None):
        """
        Build query for daily search console metrics
        
        Args:
            start_date (date): Start date
            end_date (date): End date
            domain (str, optional): Domain to filter by
            
        Returns:
            str: SQL query
        """
        domain_filter = f"AND (url LIKE '%{domain}%' OR page_path LIKE '%{domain}%')" if domain else ""
        
        return f"""
        SELECT 
            DATE(date) AS date,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS average_ctr,
            AVG(position) AS average_position
        FROM 
            `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE 
            DATE(date) BETWEEN '{start_date}' AND '{end_date}'
            {domain_filter}
        GROUP BY
            DATE(date)
        ORDER BY
            date DESC
        """
