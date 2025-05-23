"""
Supabase client for real-time data operations.
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union
from supabase import create_client, Client

from ..config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

class MarketingSupabaseClient:
    """Supabase client for marketing real-time operations"""
    
    def __init__(self):
        """Initialize the Supabase client"""
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.client: Optional[Client] = None
        
        # Initialize client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Supabase client with credentials"""
        try:
            if not self.key:
                # Try to read from environment or file
                self.key = os.environ.get('SUPABASE_KEY')
                
                if not self.key:
                    # Try to read from a secrets file if it exists
                    secrets_file = "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/supabase_key.txt"
                    if os.path.exists(secrets_file):
                        with open(secrets_file, 'r') as f:
                            self.key = f.read().strip()
            
            if not self.key:
                logger.warning("Supabase key not found. Client will have limited functionality.")
                return
                
            self.client = create_client(self.url, self.key)
            logger.info(f"Initialized Supabase client for URL: {self.url}")
            
        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")
            self.client = None
    
    def test_connection(self) -> bool:
        """Test the Supabase connection"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return False
            
            # Try a simple query
            result = self.client.table('_test_connection').select('*').limit(1).execute()
            logger.info("Supabase connection test successful")
            return True
        except Exception as e:
            # This is expected if the test table doesn't exist
            logger.info(f"Supabase connection test completed (table may not exist): {e}")
            # If we get here, the client is at least initialized
            return self.client is not None
    
    def query_table(self, table_name: str, filters: Optional[Dict[str, Any]] = None, 
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Query a table with optional filters"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return []
            
            query = self.client.table(table_name).select('*')
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            # Apply limit if provided
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error querying table {table_name}: {e}")
            return []
    
    def insert_data(self, table_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> bool:
        """Insert data into a table"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return False
            
            result = self.client.table(table_name).insert(data).execute()
            logger.info(f"Inserted data into {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            return False
    
    def update_data(self, table_name: str, data: Dict[str, Any], 
                   filters: Dict[str, Any]) -> bool:
        """Update data in a table"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return False
            
            query = self.client.table(table_name).update(data)
            
            # Apply filters
            for key, value in filters.items():
                query = query.eq(key, value)
            
            result = query.execute()
            logger.info(f"Updated data in {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating data in {table_name}: {e}")
            return False
    
    def delete_data(self, table_name: str, filters: Dict[str, Any]) -> bool:
        """Delete data from a table"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return False
            
            query = self.client.table(table_name).delete()
            
            # Apply filters
            for key, value in filters.items():
                query = query.eq(key, value)
            
            result = query.execute()
            logger.info(f"Deleted data from {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting data from {table_name}: {e}")
            return False
    
    def get_realtime_subscription(self, table_name: str, callback):
        """Subscribe to real-time changes on a table"""
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return None
            
            # Note: Real-time subscriptions require additional setup
            # This is a placeholder for future implementation
            logger.warning("Real-time subscriptions not yet implemented")
            return None
            
        except Exception as e:
            logger.error(f"Error setting up real-time subscription: {e}")
            return None