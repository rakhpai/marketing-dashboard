"""
Domain specific queries for Search Console data.
"""

from .base_queries import SearchConsoleQueries
import pandas as pd
import logging
from google.cloud import bigquery

# Set up logging
logger = logging.getLogger(__name__)

class DomainQueries:
    """Queries for specific domains and domain comparisons"""
    
    def __init__(self, credentials_path=None):
        """Initialize with base query client"""
        self.base_client = SearchConsoleQueries(credentials_path)
        
    def get_available_domains(self):
        """
        Get list of available domains in the search console data
        
        Returns:
            list: List of domains
        """
        logger.info("Getting available domains")
        
        query = """
        SELECT 
            DISTINCT REGEXP_EXTRACT(url, r'https?://([^/]+)') AS domain
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            url IS NOT NULL
        ORDER BY 
            domain
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            domains = [row.domain for row in results if row.domain]
            return domains
        except Exception as e:
            logger.error(f"Error getting available domains: {e}")
            return []
            
    def get_domain_comparison(self, domains, days_back=30):
        """
        Compare metrics for multiple domains
        
        Args:
            domains (list): List of domains to compare
            days_back (int): Number of days to look back
            
        Returns:
            pd.DataFrame: DataFrame with metrics for each domain
        """
        if not domains:
            logger.warning("No domains provided for comparison")
            return pd.DataFrame()
            
        logger.info(f"Comparing {len(domains)} domains for last {days_back} days")
        
        # Create a SQL CASE statement for each domain
        domain_cases = []
        for domain in domains:
            domain_case = f"""
            SUM(CASE WHEN REGEXP_EXTRACT(url, r'https?://([^/]+)') = '{domain}' THEN clicks ELSE 0 END) AS {domain.replace('.', '_')}_clicks,
            SUM(CASE WHEN REGEXP_EXTRACT(url, r'https?://([^/]+)') = '{domain}' THEN impressions ELSE 0 END) AS {domain.replace('.', '_')}_impressions,
            SAFE_DIVIDE(
                SUM(CASE WHEN REGEXP_EXTRACT(url, r'https?://([^/]+)') = '{domain}' THEN clicks ELSE 0 END),
                SUM(CASE WHEN REGEXP_EXTRACT(url, r'https?://([^/]+)') = '{domain}' THEN impressions ELSE 0 END)
            ) AS {domain.replace('.', '_')}_ctr,
            AVG(CASE WHEN REGEXP_EXTRACT(url, r'https?://([^/]+)') = '{domain}' THEN position ELSE NULL END) AS {domain.replace('.', '_')}_position
            """
            domain_cases.append(domain_case)
            
        domain_case_sql = ",\n            ".join(domain_cases)
        
        query = f"""
        SELECT 
            DATE(date) AS date,
            {domain_case_sql}
        FROM 
            `gtm-management-twelvetransfers.seo_data.search_console_data`
        WHERE 
            DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        GROUP BY
            DATE(date)
        ORDER BY
            date DESC
        """
        
        try:
            query_job = self.base_client.client.query(query)
            results = query_job.result()
            return results.to_dataframe()
        except Exception as e:
            logger.error(f"Error comparing domains: {e}")
            return pd.DataFrame()
