"""
Time period specific queries for Search Console data.
"""

from .base_queries import SearchConsoleQueries
import pandas as pd
import logging

# Set up logging
logger = logging.getLogger(__name__)

class TimePeriodQueries:
    """Queries for specific time periods (7, 30, 90 days)"""
    
    def __init__(self, credentials_path=None):
        """Initialize with base query client"""
        self.base_client = SearchConsoleQueries(credentials_path)
        
    def get_last_7_days_metrics(self, domain=None):
        """
        Get search console metrics for the last 7 days
        
        Args:
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with search console metrics
        """
        logger.info("Getting metrics for last 7 days")
        return self.base_client.get_search_console_metrics(7, domain)
        
    def get_last_30_days_metrics(self, domain=None):
        """
        Get search console metrics for the last 30 days
        
        Args:
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with search console metrics
        """
        logger.info("Getting metrics for last 30 days")
        return self.base_client.get_search_console_metrics(30, domain)
        
    def get_last_90_days_metrics(self, domain=None):
        """
        Get search console metrics for the last 90 days
        
        Args:
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with search console metrics
        """
        logger.info("Getting metrics for last 90 days")
        return self.base_client.get_search_console_metrics(90, domain)
        
    def get_all_time_periods(self, domain=None):
        """
        Get search console metrics for all time periods (7, 30, 90 days)
        
        Args:
            domain (str, optional): Domain to filter by
            
        Returns:
            dict: Dictionary with DataFrames for each time period
        """
        logger.info("Getting metrics for all time periods")
        
        return {
            "last_7_days": self.get_last_7_days_metrics(domain),
            "last_30_days": self.get_last_30_days_metrics(domain),
            "last_90_days": self.get_last_90_days_metrics(domain)
        }
        
    def get_daily_metrics_for_period(self, days_back, domain=None):
        """
        Get daily search console metrics for the specified period
        
        Args:
            days_back (int): Number of days to look back
            domain (str, optional): Domain to filter by
            
        Returns:
            pd.DataFrame: DataFrame with daily search console metrics
        """
        logger.info(f"Getting daily metrics for last {days_back} days")
        return self.base_client.get_daily_metrics(days_back, domain)
        
    def get_all_daily_metrics(self, domain=None):
        """
        Get daily search console metrics for all time periods (7, 30, 90 days)
        
        Args:
            domain (str, optional): Domain to filter by
            
        Returns:
            dict: Dictionary with DataFrames for each time period
        """
        logger.info("Getting daily metrics for all time periods")
        
        return {
            "last_7_days": self.get_daily_metrics_for_period(7, domain),
            "last_30_days": self.get_daily_metrics_for_period(30, domain),
            "last_90_days": self.get_daily_metrics_for_period(90, domain)
        }
