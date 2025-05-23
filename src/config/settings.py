from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # BigQuery Settings
    google_credentials_path: str = "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/credentials/seo-integration-key.json"
    bigquery_project_id: str = "gtm-management-twelvetransfers"
    bigquery_dataset: str = "seo_data"
    
    # Supabase Settings
    supabase_url: str = "https://haghsjehtqohxcvklovx.supabase.co"
    supabase_key: Optional[str] = None
    
    # API Settings
    api_base_url: str = "https://fgtwelve.ltd/api/v1"
    
    # Application Settings
    debug: bool = False
    log_level: str = "INFO"
    cache_ttl: int = 300  # 5 minutes default
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single instance of settings
settings = Settings()