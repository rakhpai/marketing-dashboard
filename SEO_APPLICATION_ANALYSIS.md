# SEO Application Technical Analysis & Schema Documentation

## Executive Summary

This document provides a comprehensive analysis of the `/var/www/vhosts/fgtwelve.ltd/seo_application` directory, extracting all database schemas, API configurations, authentication patterns, and implementation details required for marketing dashboard integration.

## Table of Contents

1. [Database Schemas](#database-schemas)
2. [Authentication & API Keys](#authentication--api-keys)
3. [Data Models & Structures](#data-models--structures)
4. [SQL Query Patterns](#sql-query-patterns)
5. [Configuration Management](#configuration-management)
6. [Integration Endpoints](#integration-endpoints)
7. [Dependencies & Requirements](#dependencies--requirements)
8. [Implementation Guidelines](#implementation-guidelines)

---

## Database Schemas

### BigQuery Database Schema

**Project**: `gtm-management-twelvetransfers`  
**Dataset**: `seo_data`  
**Location**: `US`

#### 1. Search Console Data Table
```sql
CREATE TABLE IF NOT EXISTS `gtm-management-twelvetransfers.seo_data.search_console_data` (
  date DATE NOT NULL,
  page STRING,
  query STRING,
  country STRING(2), -- ISO country code
  device STRING(7), -- 'DESKTOP', 'MOBILE', 'TABLET'
  clicks INT64 NOT NULL DEFAULT 0,
  impressions INT64 NOT NULL DEFAULT 0,
  ctr FLOAT64, -- Click-through rate (0-1)
  position FLOAT64, -- Average position (1-100+)
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Partitioning and clustering for performance
-- PARTITION BY date
-- CLUSTER BY query, page, country
```

**Key Columns**:
- `date`: Daily data aggregation
- `page`: Landing page URL
- `query`: Search query term
- `country`: Two-letter country code
- `device`: Device category
- `clicks`: Number of clicks from search results
- `impressions`: Number of times shown in search results
- `ctr`: Click-through rate (clicks/impressions)
- `position`: Average ranking position

#### 2. Keyword Tracking Table
```sql
CREATE TABLE IF NOT EXISTS `gtm-management-twelvetransfers.seo_data.keyword_tracking` (
  id STRING NOT NULL, -- UUID format
  keyword STRING NOT NULL,
  search_engine STRING DEFAULT 'google.com',
  last_checked TIMESTAMP,
  our_position INT64, -- Position of our site (1-100+)
  our_title STRING, -- Title of our ranking page
  our_link STRING, -- URL of our ranking page
  our_description STRING, -- Meta description of our page
  total_results INT64, -- Total search results count
  total_positions INT64, -- Number of positions tracked
  tag STRING, -- Category/group tag
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

**Key Columns**:
- `id`: Unique identifier (UUID)
- `keyword`: Target keyword phrase
- `our_position`: Current ranking position for our site
- `tag`: Keyword categorization

#### 3. Organic Results Table
```sql
CREATE TABLE IF NOT EXISTS `gtm-management-twelvetransfers.seo_data.organic_results` (
  id STRING NOT NULL,
  keyword_id STRING NOT NULL, -- Foreign key to keyword_tracking
  position INT64 NOT NULL, -- SERP position (1-100)
  title STRING,
  link STRING NOT NULL,
  description STRING,
  is_our_site BOOL DEFAULT FALSE, -- Flag for our domain
  date_checked TIMESTAMP,
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

**Relationships**:
- `keyword_id` → `keyword_tracking.id` (Many-to-One)

#### 4. Related Questions Table
```sql
CREATE TABLE IF NOT EXISTS `gtm-management-twelvetransfers.seo_data.related_questions` (
  id STRING NOT NULL,
  keyword_id STRING NOT NULL, -- Foreign key to keyword_tracking
  position INT64 NOT NULL, -- Position in "People also ask"
  title STRING NOT NULL, -- Question text
  link STRING, -- Answer source URL
  description STRING, -- Answer snippet
  date_checked TIMESTAMP,
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

### Supabase Database Schema (PostgreSQL)

**URL**: `https://haghsjehtqohxcvklovx.supabase.co`  
**Schema**: `public`

#### 1. Keyword Tracking Table (Supabase)
```sql
CREATE TABLE IF NOT EXISTS public.keyword_tracking (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    search_engine TEXT DEFAULT 'google.com',
    last_checked TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT keyword_search_engine_unique UNIQUE (keyword, search_engine)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_keyword_tracking_keyword ON public.keyword_tracking(keyword);
CREATE INDEX IF NOT EXISTS idx_keyword_tracking_last_checked ON public.keyword_tracking(last_checked);
```

#### 2. Organic Results Table (Supabase)
```sql
CREATE TABLE IF NOT EXISTS public.organic_results (
    id SERIAL PRIMARY KEY,
    keyword_id INTEGER NOT NULL REFERENCES public.keyword_tracking(id) ON DELETE CASCADE,
    position INTEGER NOT NULL CHECK (position > 0),
    link TEXT NOT NULL,
    title TEXT,
    description TEXT,
    is_our_site BOOLEAN DEFAULT FALSE,
    date_checked TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_keyword_position_date UNIQUE (keyword_id, position, date_checked)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_organic_results_keyword_id ON public.organic_results(keyword_id);
CREATE INDEX IF NOT EXISTS idx_organic_results_position ON public.organic_results(position);
CREATE INDEX IF NOT EXISTS idx_organic_results_our_site ON public.organic_results(is_our_site);
CREATE INDEX IF NOT EXISTS idx_organic_results_date_checked ON public.organic_results(date_checked);
```

#### 3. Search Console Data Table (Supabase)
```sql
CREATE TABLE IF NOT EXISTS public.search_console_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    page TEXT,
    query TEXT,
    country CHAR(2), -- ISO country code
    device VARCHAR(10) CHECK (device IN ('DESKTOP', 'MOBILE', 'TABLET')),
    clicks INTEGER NOT NULL DEFAULT 0 CHECK (clicks >= 0),
    impressions INTEGER NOT NULL DEFAULT 0 CHECK (impressions >= 0),
    ctr NUMERIC(5,4) CHECK (ctr >= 0 AND ctr <= 1), -- 4 decimal places
    position NUMERIC(6,2) CHECK (position > 0), -- 2 decimal places
    imported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_search_console_record UNIQUE (date, page, query, country, device)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_search_console_data_date ON public.search_console_data(date);
CREATE INDEX IF NOT EXISTS idx_search_console_data_query ON public.search_console_data(query);
CREATE INDEX IF NOT EXISTS idx_search_console_data_page ON public.search_console_data(page);
CREATE INDEX IF NOT EXISTS idx_search_console_data_country ON public.search_console_data(country);
CREATE INDEX IF NOT EXISTS idx_search_console_data_device ON public.search_console_data(device);
```

---

## Authentication & API Keys

### Service Account Configuration

#### Primary Credentials Path
```bash
# Production environment
GOOGLE_APPLICATION_CREDENTIALS="/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json"
```

#### Fallback Credential Paths
```python
ALTERNATIVE_CREDENTIALS_PATHS = [
    "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json",  # Primary
    "/var/www/vhosts/fgtwelve.ltd/seo_application/seo-twelve/seo-integration-key.json",  # Backup
    "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/seo-integration-key.json"  # Local copy
]
```

#### Environment Variables
```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID="gtm-management-twelvetransfers"
GOOGLE_APPLICATION_CREDENTIALS="/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json"
BIGQUERY_DATASET_ID="seo_data"
BIGQUERY_LOCATION="US"

# Supabase Configuration
SUPABASE_URL="https://haghsjehtqohxcvklovx.supabase.co"
SUPABASE_KEY="your_supabase_anon_key_here"

# Application Configuration
STREAMLIT_ENV="production"
LOG_LEVEL="INFO"
CACHE_TTL="3600"
```

#### Authentication Implementation Pattern
```python
# File: src/data/bigquery_client.py
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path

class BigQueryAuthenticator:
    def __init__(self, settings):
        self.settings = settings
        self.credentials = None
        self.client = None
        
    def _find_credentials_file(self):
        """Find valid credentials file from multiple paths"""
        potential_paths = [
            self.settings.google_application_credentials,
            "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json",
            "/var/www/vhosts/fgtwelve.ltd/seo_application/seo-twelve/seo-integration-key.json"
        ]
        
        for path in potential_paths:
            if path and Path(path).exists():
                return path
        
        raise FileNotFoundError("No valid Google Cloud credentials file found")
    
    def initialize_client(self):
        """Initialize BigQuery client with service account credentials"""
        try:
            credentials_file = self._find_credentials_file()
            
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_file,
                scopes=[
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/cloud-platform"
                ]
            )
            
            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.settings.google_cloud_project_id,
                location=self.settings.bigquery_location
            )
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize BigQuery client: {e}")
    
    def _test_connection(self):
        """Test BigQuery connection"""
        test_query = "SELECT 1 as test_connection"
        try:
            result = list(self.client.query(test_query).result())
            assert len(result) == 1
        except Exception as e:
            raise ConnectionError(f"BigQuery connection test failed: {e}")
```

### Supabase Authentication
```python
# File: src/data/supabase_client.py
import os
import requests
from typing import Dict, List, Optional

class SupabaseAuthenticator:
    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.environ.get("SUPABASE_URL")
        self.key = key or os.environ.get("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key are required")
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for Supabase API requests"""
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def test_connection(self) -> bool:
        """Test Supabase connection"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
```

---

## Data Models & Structures

### Pydantic Settings Configuration
```python
# File: src/config/settings.py
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional, List
from pathlib import Path
import os

class Settings(BaseSettings):
    """Application settings with validation and environment configuration"""
    
    # Environment
    streamlit_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    
    # Google Cloud / BigQuery
    google_cloud_project_id: str = "gtm-management-twelvetransfers"
    google_application_credentials: str = ""
    bigquery_dataset_id: str = "seo_data"
    bigquery_location: str = "US"
    
    # Supabase
    supabase_url: str = "https://haghsjehtqohxcvklovx.supabase.co"
    supabase_key: Optional[str] = None
    
    # Application Performance
    cache_ttl: int = 3600  # 1 hour
    max_rows_display: int = 10000
    chunk_size: int = 10000
    max_concurrent_queries: int = 5
    
    # UI Configuration
    page_title: str = "Marketing Analytics Dashboard"
    page_icon: str = "📊"
    layout: str = "wide"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._configure_credentials_path()
    
    def _configure_credentials_path(self):
        """Configure Google Cloud credentials path based on environment"""
        if not self.google_application_credentials:
            if self.streamlit_env == "production":
                self.google_application_credentials = "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json"
            else:
                # Development fallback
                project_root = Path(__file__).parents[2]
                self.google_application_credentials = str(project_root / "seo-integration-key.json")
    
    @field_validator('google_application_credentials')
    @classmethod
    def validate_credentials_file(cls, v):
        """Validate that credentials file exists"""
        if v and not Path(v).exists():
            # Don't raise error, just log warning for fallback handling
            pass
        return v
    
    @field_validator('streamlit_env')
    @classmethod
    def validate_environment(cls, v):
        """Validate environment setting"""
        valid_envs = ['development', 'staging', 'production']
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v
    
    @property
    def is_production(self) -> bool:
        return self.streamlit_env == "production"
    
    @property
    def is_development(self) -> bool:
        return self.streamlit_env == "development"

# Singleton settings instance
settings = Settings()
```

### Data Transfer Objects (DTOs)
```python
# File: src/models/data_models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal

class SearchConsoleRecord(BaseModel):
    """Search Console data record"""
    date: date
    page: Optional[str] = None
    query: Optional[str] = None
    country: Optional[str] = Field(None, max_length=2)
    device: Optional[str] = Field(None, regex="^(DESKTOP|MOBILE|TABLET)$")
    clicks: int = Field(0, ge=0)
    impressions: int = Field(0, ge=0)
    ctr: Optional[Decimal] = Field(None, ge=0, le=1)
    position: Optional[Decimal] = Field(None, gt=0)
    imported_at: Optional[datetime] = None

class KeywordTrackingRecord(BaseModel):
    """Keyword tracking record"""
    id: Optional[str] = None
    keyword: str
    search_engine: str = "google.com"
    last_checked: Optional[datetime] = None
    our_position: Optional[int] = Field(None, gt=0)
    our_title: Optional[str] = None
    our_link: Optional[str] = None
    our_description: Optional[str] = None
    total_results: Optional[int] = Field(None, ge=0)
    total_positions: Optional[int] = Field(None, ge=0)
    tag: Optional[str] = None
    imported_at: Optional[datetime] = None

class OrganicResultRecord(BaseModel):
    """Organic search result record"""
    id: Optional[str] = None
    keyword_id: str
    position: int = Field(gt=0)
    title: Optional[str] = None
    link: str
    description: Optional[str] = None
    is_our_site: bool = False
    date_checked: Optional[datetime] = None
    imported_at: Optional[datetime] = None

class QueryResult(BaseModel):
    """Generic query result container"""
    data: List[Dict[str, Any]]
    total_rows: int
    query_time_ms: Optional[int] = None
    cached: bool = False
```

---

## SQL Query Patterns

### Core Analytics Queries
```python
# File: src/data/queries.py
from typing import Optional, Dict, Any
from src.config.settings import settings

class SEOAnalyticsQueries:
    """Centralized query definitions for SEO analytics"""
    
    @staticmethod
    def daily_search_performance(
        start_date: str, 
        end_date: str, 
        country: Optional[str] = None,
        device: Optional[str] = None
    ) -> str:
        """Daily aggregated search console performance"""
        where_clauses = [
            f"date BETWEEN '{start_date}' AND '{end_date}'"
        ]
        
        if country:
            where_clauses.append(f"country = '{country}'")
        if device:
            where_clauses.append(f"device = '{device}'")
        
        where_clause = " AND ".join(where_clauses)
        
        return f"""
        SELECT
            date,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100 AS avg_ctr_percent,
            SAFE_DIVIDE(SUM(position * impressions), SUM(impressions)) AS weighted_avg_position,
            COUNT(DISTINCT query) AS unique_queries,
            COUNT(DISTINCT page) AS unique_pages,
            COUNT(DISTINCT country) AS unique_countries
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
        WHERE
            {where_clause}
        GROUP BY date
        ORDER BY date ASC
        """
    
    @staticmethod
    def top_performing_keywords(
        days_back: int = 30, 
        limit: int = 100,
        min_clicks: int = 1
    ) -> str:
        """Top performing keywords by clicks"""
        return f"""
        SELECT
            query,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100 AS ctr_percent,
            SAFE_DIVIDE(SUM(position * impressions), SUM(impressions)) AS weighted_avg_position,
            COUNT(DISTINCT page) AS landing_pages,
            COUNT(DISTINCT country) AS countries,
            MAX(date) AS last_seen
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
        WHERE
            date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND query IS NOT NULL 
            AND query != ''
        GROUP BY query
        HAVING total_clicks >= {min_clicks}
        ORDER BY total_clicks DESC
        LIMIT {limit}
        """
    
    @staticmethod
    def page_performance_analysis(days_back: int = 30) -> str:
        """Page-level performance analysis"""
        return f"""
        SELECT
            page,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100 AS ctr_percent,
            SAFE_DIVIDE(SUM(position * impressions), SUM(impressions)) AS weighted_avg_position,
            COUNT(DISTINCT query) AS ranking_keywords,
            COUNT(DISTINCT country) AS countries,
            -- Performance trends
            SAFE_DIVIDE(
                SUM(CASE WHEN date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) THEN clicks ELSE 0 END),
                SUM(CASE WHEN date < DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) 
                         AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY) THEN clicks ELSE 0 END)
            ) - 1 AS weekly_clicks_growth_rate
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
        WHERE
            date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
            AND page IS NOT NULL
        GROUP BY page
        HAVING total_clicks > 0
        ORDER BY total_clicks DESC
        """
    
    @staticmethod
    def keyword_position_tracking() -> str:
        """Our current keyword positions"""
        return f"""
        SELECT
            kt.keyword,
            kt.search_engine,
            kt.our_position,
            kt.our_title,
            kt.our_link,
            kt.tag,
            kt.last_checked,
            -- Competitor analysis
            COUNT(org.id) AS total_competitors,
            COUNT(CASE WHEN org.position < kt.our_position THEN 1 END) AS competitors_above,
            MIN(org.position) AS best_competitor_position,
            -- Search volume estimate from search console
            COALESCE(sc.avg_impressions, 0) AS estimated_monthly_searches
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.keyword_tracking` kt
        LEFT JOIN
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.organic_results` org
            ON kt.id = org.keyword_id AND org.is_our_site = FALSE
        LEFT JOIN (
            SELECT 
                query,
                AVG(impressions) * 30 AS avg_impressions
            FROM 
                `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
            WHERE 
                date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            GROUP BY query
        ) sc ON kt.keyword = sc.query
        WHERE
            kt.our_position IS NOT NULL
        GROUP BY
            kt.keyword, kt.search_engine, kt.our_position, kt.our_title, 
            kt.our_link, kt.tag, kt.last_checked, sc.avg_impressions
        ORDER BY
            kt.our_position ASC, estimated_monthly_searches DESC
        """
    
    @staticmethod
    def conversion_funnel_analysis(days_back: int = 30) -> str:
        """Search to conversion funnel analysis"""
        return f"""
        WITH search_metrics AS (
            SELECT
                SUM(impressions) AS total_impressions,
                SUM(clicks) AS total_clicks,
                COUNT(DISTINCT query) AS unique_queries
            FROM
                `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
            WHERE
                date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        ),
        top_keywords AS (
            SELECT
                query,
                SUM(clicks) AS clicks,
                SUM(impressions) AS impressions,
                SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS ctr
            FROM
                `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
            WHERE
                date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
                AND query IS NOT NULL
            GROUP BY query
            HAVING clicks > 0
            ORDER BY clicks DESC
            LIMIT 10
        )
        SELECT
            'Total' AS metric_type,
            total_impressions AS impressions,
            total_clicks AS clicks,
            SAFE_DIVIDE(total_clicks, total_impressions) * 100 AS ctr_percent,
            unique_queries
        FROM search_metrics
        UNION ALL
        SELECT
            'Top Keywords' AS metric_type,
            SUM(impressions) AS impressions,
            SUM(clicks) AS clicks,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100 AS ctr_percent,
            COUNT(*) AS unique_queries
        FROM top_keywords
        """

class PerformanceQueries:
    """Queries optimized for dashboard performance"""
    
    @staticmethod
    def cached_daily_summary() -> str:
        """Pre-aggregated daily summary for fast loading"""
        return f"""
        SELECT
            date,
            total_clicks,
            total_impressions,
            avg_ctr_percent,
            avg_position,
            unique_queries,
            unique_pages
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.daily_summary_cache`
        WHERE
            date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        ORDER BY date DESC
        """
    
    @staticmethod
    def create_daily_summary_cache() -> str:
        """Create/update daily summary cache table"""
        return f"""
        CREATE OR REPLACE TABLE 
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.daily_summary_cache`
        AS
        SELECT
            date,
            SUM(clicks) AS total_clicks,
            SUM(impressions) AS total_impressions,
            SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100 AS avg_ctr_percent,
            SAFE_DIVIDE(SUM(position * impressions), SUM(impressions)) AS avg_position,
            COUNT(DISTINCT query) AS unique_queries,
            COUNT(DISTINCT page) AS unique_pages,
            CURRENT_TIMESTAMP() AS cache_updated_at
        FROM
            `{settings.google_cloud_project_id}.{settings.bigquery_dataset_id}.search_console_data`
        WHERE
            date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
        GROUP BY date
        ORDER BY date
        """
```

### Supabase Queries
```python
# File: src/data/supabase_queries.py
class SupabaseQueries:
    """Supabase-specific query patterns"""
    
    @staticmethod
    def get_search_console_paginated(offset: int = 0, limit: int = 1000) -> str:
        """Paginated search console data retrieval"""
        return f"""
        SELECT *
        FROM search_console_data
        ORDER BY date DESC, imported_at DESC
        LIMIT {limit}
        OFFSET {offset}
        """
    
    @staticmethod
    def get_keyword_tracking_active() -> str:
        """Get active keyword tracking records"""
        return """
        SELECT 
            kt.*,
            COUNT(org.id) as result_count
        FROM keyword_tracking kt
        LEFT JOIN organic_results org ON kt.id = org.keyword_id
        WHERE kt.last_checked >= NOW() - INTERVAL '7 days'
        GROUP BY kt.id, kt.keyword, kt.search_engine, kt.last_checked, kt.created_at, kt.updated_at
        ORDER BY kt.last_checked DESC
        """
    
    @staticmethod
    def get_our_ranking_positions() -> str:
        """Get positions where our site ranks"""
        return """
        SELECT 
            kt.keyword,
            org.position,
            org.title,
            org.link,
            org.description,
            org.date_checked
        FROM keyword_tracking kt
        JOIN organic_results org ON kt.id = org.keyword_id
        WHERE org.is_our_site = true
        ORDER BY org.position ASC, org.date_checked DESC
        """
```

---

## Configuration Management

### Application Configuration Structure
```python
# File: src/config/app_config.py
from dataclasses import dataclass
from typing import Dict, List, Optional
import os

@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    bigquery_project_id: str
    bigquery_dataset_id: str
    bigquery_location: str
    supabase_url: str
    supabase_key: str
    credentials_path: str

@dataclass
class UIConfig:
    """User interface configuration"""
    page_title: str = "Marketing Analytics Dashboard"
    page_icon: str = "📊"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    theme: str = "light"
    
@dataclass
class PerformanceConfig:
    """Performance and caching configuration"""
    cache_ttl: int = 3600
    max_rows_display: int = 10000
    chunk_size: int = 10000
    max_concurrent_queries: int = 5
    enable_caching: bool = True

@dataclass
class FeatureFlags:
    """Feature toggle configuration"""
    enable_real_time_updates: bool = True
    enable_predictive_analytics: bool = False
    enable_competitor_analysis: bool = True
    enable_geographic_analysis: bool = True
    enable_export_functionality: bool = True

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, env: str = "production"):
        self.env = env
        self.database = self._load_database_config()
        self.ui = self._load_ui_config()
        self.performance = self._load_performance_config()
        self.features = self._load_feature_flags()
    
    def _load_database_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            bigquery_project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID", "gtm-management-twelvetransfers"),
            bigquery_dataset_id=os.getenv("BIGQUERY_DATASET_ID", "seo_data"),
            bigquery_location=os.getenv("BIGQUERY_LOCATION", "US"),
            supabase_url=os.getenv("SUPABASE_URL", "https://haghsjehtqohxcvklovx.supabase.co"),
            supabase_key=os.getenv("SUPABASE_KEY", ""),
            credentials_path=os.getenv(
                "GOOGLE_APPLICATION_CREDENTIALS", 
                "/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json"
            )
        )
    
    def _load_ui_config(self) -> UIConfig:
        return UIConfig(
            page_title=os.getenv("APP_TITLE", "Marketing Analytics Dashboard"),
            layout=os.getenv("STREAMLIT_LAYOUT", "wide"),
            theme=os.getenv("UI_THEME", "light")
        )
    
    def _load_performance_config(self) -> PerformanceConfig:
        return PerformanceConfig(
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            max_rows_display=int(os.getenv("MAX_ROWS_DISPLAY", "10000")),
            enable_caching=os.getenv("ENABLE_CACHING", "true").lower() == "true"
        )
    
    def _load_feature_flags(self) -> FeatureFlags:
        return FeatureFlags(
            enable_real_time_updates=os.getenv("ENABLE_REAL_TIME", "true").lower() == "true",
            enable_predictive_analytics=os.getenv("ENABLE_PREDICTIONS", "false").lower() == "true",
            enable_competitor_analysis=os.getenv("ENABLE_COMPETITORS", "true").lower() == "true"
        )
```

---

## Integration Endpoints

### BigQuery Integration Points
```python
# File: src/integrations/bigquery_integration.py
from google.cloud import bigquery
from typing import List, Dict, Any, Optional
import pandas as pd
from src.config.settings import settings

class BigQueryIntegration:
    """Production-ready BigQuery integration"""
    
    def __init__(self):
        self.client = None
        self.project_id = settings.google_cloud_project_id
        self.dataset_id = settings.bigquery_dataset_id
        self._initialize_client()
    
    def execute_query(self, query: str, use_cache: bool = True) -> pd.DataFrame:
        """Execute query with caching and error handling"""
        try:
            job_config = bigquery.QueryJobConfig(
                use_query_cache=use_cache,
                use_legacy_sql=False
            )
            
            query_job = self.client.query(query, job_config=job_config)
            result = query_job.result()
            
            return result.to_dataframe()
            
        except Exception as e:
            raise QueryExecutionError(f"BigQuery execution failed: {e}")
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get table schema information"""
        table_ref = self.client.dataset(self.dataset_id).table(table_name)
        table = self.client.get_table(table_ref)
        
        return [
            {
                "name": field.name,
                "type": field.field_type,
                "mode": field.mode,
                "description": field.description or ""
            }
            for field in table.schema
        ]
    
    def create_table_if_not_exists(self, table_name: str, schema: List[bigquery.SchemaField]):
        """Create table with specified schema if it doesn't exist"""
        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        
        try:
            self.client.get_table(table_id)
        except:
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            print(f"Created table {table_id}")
```

### Supabase Integration Points
```python
# File: src/integrations/supabase_integration.py
import requests
from typing import List, Dict, Any, Optional
import pandas as pd
from src.config.settings import settings

class SupabaseIntegration:
    """Production-ready Supabase integration"""
    
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def execute_select(self, table: str, select: str = "*", 
                      where: Optional[str] = None, 
                      order: Optional[str] = None,
                      limit: Optional[int] = None,
                      offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query with filters"""
        
        url = f"{self.url}/rest/v1/{table}"
        params = {"select": select}
        
        if where:
            params.update(self._parse_where_clause(where))
        if order:
            params["order"] = order
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def insert_batch(self, table: str, data: List[Dict[str, Any]]) -> bool:
        """Insert multiple records"""
        url = f"{self.url}/rest/v1/{table}"
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return True
    
    def get_table_info(self, table: str) -> Dict[str, Any]:
        """Get table metadata"""
        # This would typically use Supabase's metadata endpoints
        # For now, return basic structure
        return {
            "table_name": table,
            "row_count": self._get_row_count(table)
        }
    
    def _get_row_count(self, table: str) -> int:
        """Get total row count for table"""
        url = f"{self.url}/rest/v1/{table}"
        headers = {**self.headers, "Prefer": "count=exact"}
        
        response = requests.head(url, headers=headers)
        response.raise_for_status()
        
        content_range = response.headers.get("Content-Range", "")
        if "/" in content_range:
            return int(content_range.split("/")[1])
        return 0
```

---

## Dependencies & Requirements

### Core Dependencies
```text
# requirements.txt - Complete dependency list

# Streamlit Framework
streamlit>=1.28.0,<2.0.0

# Data Processing
pandas>=1.3.0,<2.0.0
numpy>=1.20.0,<2.0.0

# Google Cloud
google-cloud-bigquery>=3.9.0,<4.0.0
google-cloud-bigquery-storage>=2.31.0,<3.0.0
google-auth>=2.0.0,<3.0.0
google-auth-oauthlib>=0.4.6,<1.0.0
google-api-python-client>=2.0.0,<3.0.0
pandas-gbq>=0.19.0,<1.0.0

# Database
supabase>=2.0.0,<3.0.0
pyarrow>=12.0.0,<13.0.0
db-dtypes>=1.1.1,<2.0.0

# Configuration
pydantic>=1.10.0,<2.0.0
pydantic-settings>=2.0.0,<3.0.0

# Visualization
plotly>=5.13.0,<6.0.0
matplotlib>=3.4.0,<4.0.0

# HTTP Requests
requests>=2.25.0,<3.0.0

# Utilities
python-dotenv>=1.0.0,<2.0.0
pathlib2>=2.3.0,<3.0.0  # For Python < 3.8 compatibility

# Development Dependencies (optional)
pytest>=7.0.0,<8.0.0
pytest-mock>=3.10.0,<4.0.0
black>=23.0.0,<24.0.0
flake8>=6.0.0,<7.0.0
mypy>=1.0.0,<2.0.0
```

### Environment Setup Script
```bash
#!/bin/bash
# setup_environment.sh

set -e

echo "Setting up Marketing Dashboard environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p cache
mkdir -p static/css
mkdir -p static/js

# Set up environment variables
if [ ! -f .env ]; then
    cat > .env << EOF
# Environment Configuration
STREAMLIT_ENV=production
LOG_LEVEL=INFO
DEBUG=false

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=gtm-management-twelvetransfers
BIGQUERY_DATASET_ID=seo_data
BIGQUERY_LOCATION=US
GOOGLE_APPLICATION_CREDENTIALS=/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json

# Supabase Configuration
SUPABASE_URL=https://haghsjehtqohxcvklovx.supabase.co
SUPABASE_KEY=your_supabase_key_here

# Performance Configuration
CACHE_TTL=3600
MAX_ROWS_DISPLAY=10000
ENABLE_CACHING=true

# UI Configuration
APP_TITLE=Marketing Analytics Dashboard
STREAMLIT_LAYOUT=wide
UI_THEME=light
EOF
    echo "Created .env file - please update with your actual values"
fi

echo "Environment setup complete!"
echo "To activate: source venv/bin/activate"
echo "To run: streamlit run app.py"
```

---

## Implementation Guidelines

### 1. Project Structure Recommendations
```
marketing/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Pydantic settings
│   │   └── app_config.py        # Application configuration
│   ├── data/
│   │   ├── __init__.py
│   │   ├── bigquery_client.py   # BigQuery integration
│   │   ├── supabase_client.py   # Supabase integration
│   │   └── queries.py           # SQL query definitions
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_models.py       # Pydantic data models
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── bigquery_integration.py
│   │   └── supabase_integration.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py            # Chart components
│   │   ├── metrics.py           # Metric components
│   │   └── ui_components.py     # UI helper components
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── overview.py          # Main dashboard
│   │   ├── keywords.py          # Keyword analysis
│   │   ├── traffic.py           # Traffic analysis
│   │   └── performance.py       # Performance metrics
│   └── utils/
│       ├── __init__.py
│       ├── cache.py             # Caching utilities
│       └── helpers.py           # Helper functions
├── static/
│   ├── css/
│   │   └── custom.css           # Custom styling
│   └── js/
│       └── custom.js            # Custom JavaScript
├── tests/
│   ├── __init__.py
│   ├── test_bigquery.py
│   ├── test_supabase.py
│   └── test_queries.py
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── setup_environment.sh         # Environment setup script
└── README.md                    # Documentation
```

### 2. Implementation Sequence
```python
# Phase 1: Foundation Setup
1. Create project structure
2. Set up configuration management (settings.py)
3. Implement authentication clients (BigQuery, Supabase)
4. Create basic data models

# Phase 2: Data Integration
1. Implement BigQuery client with queries
2. Implement Supabase client with API calls
3. Create data fetching functions
4. Add error handling and fallbacks

# Phase 3: UI Development
1. Create basic Streamlit app structure
2. Implement enhanced UI components
3. Add chart and visualization components
4. Integrate real data sources

# Phase 4: Advanced Features
1. Add caching and performance optimization
2. Implement real-time updates
3. Add predictive analytics
4. Create export functionality

# Phase 5: Production Deployment
1. Configure production environment
2. Set up systemd service
3. Update nginx configuration
4. Implement monitoring and logging
```

### 3. Key Implementation Notes

#### Authentication Best Practices
- Always use service account authentication for production
- Implement fallback credential paths for different environments
- Test connections before proceeding with data operations
- Handle authentication errors gracefully

#### Query Optimization
- Use parameterized queries to prevent SQL injection
- Implement query caching for frequently accessed data
- Use appropriate BigQuery slot management
- Consider query costs and optimize accordingly

#### Error Handling
- Implement comprehensive error handling for all external API calls
- Provide meaningful error messages to users
- Log errors appropriately for debugging
- Implement fallback mechanisms for data source failures

#### Performance Considerations
- Use connection pooling for database clients
- Implement multi-level caching (memory, Redis, file-based)
- Optimize DataFrame operations for large datasets
- Use async operations where appropriate

This comprehensive documentation provides all the schemas, patterns, and implementation details needed to successfully integrate the SEO application's proven infrastructure into your marketing dashboard.