# Search Console Queries

A Python package for querying and analyzing Google Search Console data stored in BigQuery.

## Overview

This package provides a set of tools for querying and analyzing Google Search Console data stored in BigQuery. It includes:

- Time period queries (7, 30, 90 days)
- Domain-specific queries
- Keyword analysis
- Page performance analysis
- Utility functions for formatting and visualizing data

## Installation

No installation is required. The package can be used directly from the repository.

## Authentication

The package supports two authentication methods:

1. **Service Account Key File**: Provide a path to a service account key file.
2. **Application Default Credentials**: If no credentials are provided, the package will use application default credentials.

## Usage

### Command Line Interface

The package includes a command-line interface for running queries:

```bash
# Run all queries for the last 30 days
./run_queries.py

# Run time period queries for the last 7 days
./run_queries.py --time-period --days 7

# Run keyword queries for a specific domain
./run_queries.py --keywords --domain twelvetransfers.com

# Analyze a specific keyword
./run_queries.py --keywords --keyword "airport transfer london"

# Analyze a specific page
./run_queries.py --pages --page-url "https://twelvetransfers.com/airport-transfers"

# Specify credentials file
./run_queries.py --credentials /path/to/credentials.json
```

### Python API

The package can also be used as a Python API:

```python
from search_console_queries import TimePeriodQueries, KeywordQueries

# Initialize with credentials
time_period_client = TimePeriodQueries('/path/to/credentials.json')

# Get metrics for the last 30 days
metrics_df = time_period_client.get_last_30_days_metrics()

# Get daily metrics for the last 7 days
daily_df = time_period_client.get_daily_metrics_for_period(7)

# Get top keywords
keyword_client = KeywordQueries()
top_keywords = keyword_client.get_top_keywords(days_back=30, limit=100)
```

## Available Queries

### Time Period Queries

- `get_last_7_days_metrics(domain=None)`
- `get_last_30_days_metrics(domain=None)`
- `get_last_90_days_metrics(domain=None)`
- `get_daily_metrics_for_period(days_back, domain=None)`

### Domain Queries

- `get_available_domains()`
- `get_domain_comparison(domains, days_back=30)`

### Keyword Queries

- `get_top_keywords(days_back=30, limit=100, domain=None)`
- `get_keyword_trend(keyword, days_back=90, domain=None)`
- `get_keywords_by_position_range(min_position, max_position, days_back=30, limit=100, domain=None)`

### Page Queries

- `get_top_pages(days_back=30, limit=100, domain=None)`
- `get_page_trend(page_url, days_back=90, domain=None)`
- `get_page_keywords(page_url, days_back=30, limit=100)`

## Utility Functions

- `format_metrics(df)`: Format metrics for display
- `save_to_csv(df, filename, output_dir='./output')`: Save DataFrame to CSV
- `plot_daily_metrics(df, metric_cols=None, title=None, figsize=(12, 6), output_file=None)`: Plot daily metrics
- `calculate_period_over_period_change(current_df, previous_df, metric_cols=None)`: Calculate period-over-period change
