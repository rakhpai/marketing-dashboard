"""
BigQuery client for accessing marketing analytics data.
"""

import os
import json
import logging
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPIError

from ..config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

class MarketingBigQueryClient:
    """BigQuery client for marketing analytics"""

    def __init__(self):
        """Initialize the BigQuery client"""
        self.project_id = settings.bigquery_project_id
        self.dataset_id = settings.bigquery_dataset
        self.client = None
        self.credentials = None
        
        # Initialize client with credentials
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the BigQuery client with service account credentials"""
        try:
            # Use credentials from settings
            credentials_file = settings.google_credentials_path
            
            if not os.path.exists(credentials_file):
                logger.warning(f"Primary credentials file not found: {credentials_file}")
                # Try alternative locations
                alt_credentials_files = [
                    "/var/www/vhosts/fgtwelve.ltd/seo_application/seo-twelve/seo-integration-key.json",
                    "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/seo-integration-key.json",
                    "./seo-integration-key.json"
                ]
                
                for alt_file in alt_credentials_files:
                    if os.path.exists(alt_file):
                        credentials_file = alt_file
                        logger.info(f"Using alternative credentials file: {credentials_file}")
                        break
                else:
                    logger.error("No valid credentials file found in any location")
                    raise FileNotFoundError(f"No valid credentials file found")
            
            # Fix common issues with service account keys (malformed private_key)
            try:
                with open(credentials_file, 'r') as f:
                    key_data = json.load(f)
                
                # Check if private key has the extra \n at the end
                if 'private_key' in key_data and key_data['private_key'].endswith('\\n"'):
                    # Remove the trailing \n from private_key
                    key_data['private_key'] = key_data['private_key'].rstrip('\\n"') + '"'
                    
                    # Make sure the private_key doesn't end with double newline
                    if '\\n\\n' in key_data['private_key']:
                        key_data['private_key'] = key_data['private_key'].replace('\\n\\n', '\\n')
                    
                    # Write the corrected key back
                    with open(credentials_file, 'w') as f:
                        json.dump(key_data, f, indent=2)
                        
                    logger.info(f"Fixed service account key format: {credentials_file}")
            except Exception as e:
                logger.error(f"Error fixing service account key: {e}")
                
            # Initialize the credentials
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_file,
                scopes=["https://www.googleapis.com/auth/bigquery"]
            )
            
            # Create the client
            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.project_id
            )
            
            logger.info(f"Initialized BigQuery client for project: {self.project_id}")
            
        except Exception as e:
            logger.error(f"Error initializing BigQuery client: {e}")
            self.client = None
            self.credentials = None
            raise

    def test_connection(self) -> bool:
        """Test the BigQuery connection"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized")
                return False
                
            query = "SELECT 1 as test_connection"
            result = self.client.query(query).result()
            
            # Check if we got a result
            for row in result:
                if row.test_connection == 1:
                    logger.info("BigQuery connection test successful")
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"BigQuery connection test failed: {e}")
            return False

    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """Execute a query and return the results as a DataFrame"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized. Cannot execute query.")
                return pd.DataFrame()
                
            logger.info(f"Executing query: {query[:100]}...")
            query_job = self.client.query(query)
            return query_job.to_dataframe()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()

    def check_dataset_exists(self) -> bool:
        """Check if the dataset exists and is accessible"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized. Cannot check dataset.")
                return False
                
            # Try to get the dataset
            dataset_ref = self.client.dataset(self.dataset_id)
            
            try:
                # Get the dataset
                dataset = self.client.get_dataset(dataset_ref)
                logger.info(f"Dataset {self.dataset_id} exists and is accessible")
                return True
            except Exception as e:
                error_str = str(e)
                if "Not found: Dataset" in error_str:
                    logger.warning(f"Dataset {self.dataset_id} does not exist")
                    return False
                elif "Permission denied" in error_str or "Access Denied" in error_str:
                    logger.warning(f"Permission error accessing dataset {self.dataset_id}")
                    return False
                else:
                    logger.error(f"Error getting dataset: {e}")
                    return False
        except Exception as e:
            logger.error(f"Error checking dataset: {e}")
            return False

    def list_tables(self) -> List[str]:
        """List all tables in the dataset"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized")
                return []
                
            dataset_ref = self.client.dataset(self.dataset_id)
            tables = list(self.client.list_tables(dataset_ref))
            table_names = [table.table_id for table in tables]
            logger.info(f"Found {len(table_names)} tables in dataset {self.dataset_id}")
            return table_names
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            return []

    def table_exists(self, table_name: str) -> bool:
        """Check if a specific table exists"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized")
                return False
                
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
            
            try:
                self.client.get_table(table_id)
                logger.info(f"Table {table_name} exists")
                return True
            except Exception:
                logger.info(f"Table {table_name} does not exist")
                return False
        except Exception as e:
            logger.error(f"Error checking table existence: {e}")
            return False

    def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get the schema of a table"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized")
                return []
                
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
            table = self.client.get_table(table_id)
            
            schema = []
            for field in table.schema:
                schema.append({
                    'name': field.name,
                    'type': field.field_type,
                    'mode': field.mode,
                    'description': field.description or ''
                })
            
            return schema
        except Exception as e:
            logger.error(f"Error getting table schema: {e}")
            return []

    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str,
                                write_disposition: str = "WRITE_TRUNCATE") -> bool:
        """Create or replace a table from a DataFrame"""
        try:
            if not self.client:
                logger.error("BigQuery client not initialized. Cannot create table.")
                return False
                
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"

            job_config = bigquery.LoadJobConfig(
                write_disposition=write_disposition
            )

            job = self.client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )

            job.result()  # Wait for the job to complete

            logger.info(f"Loaded {len(df)} rows into {table_id}")
            return True
        except Exception as e:
            logger.error(f"Error creating table from DataFrame: {e}")
            return False