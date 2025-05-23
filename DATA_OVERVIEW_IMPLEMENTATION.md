# BigQuery Data Overview Implementation

## Overview
The marketing dashboard now displays comprehensive BigQuery data metadata at the top of the dashboard, providing immediate visibility into data availability, freshness, and quality.

## Key Features Implemented

### 1. Data Overview Section (Always at Top)
The dashboard now starts with a "BigQuery Data Overview" section that shows:

#### Main Metrics (4 columns):
- **Column 1:**
  - Total Rows: Total number of rows in search console data
  - Unique Queries: Number of unique search queries

- **Column 2:**
  - Data Range: Shows days of data available with date range in tooltip
  - Unique Pages: Number of unique pages with data

- **Column 3:**
  - Last Data Update: Shows the date of the most recent data
  - Days Since Update: Visual indicator (red if > 3 days old)
  - Total Clicks: Total clicks across all data

- **Column 4:**
  - Total Impressions: Total impressions across all data
  - Countries: Number of countries in the data

### 2. Data Quality & Freshness (Expandable Section)
Contains two subsections:

#### Data Quality Metrics:
- Null Queries percentage
- Null Pages percentage
- Invalid CTR percentage (CTR > 100%)
- Invalid Position percentage (position < 0 or > 1000)

#### Table Freshness:
- Shows freshness for each BigQuery table
- Includes row count, latest date, and days since update
- Currently monitors:
  - search_console_data
  - keyword_positions

### 3. Daily Data Volume Chart (Expandable)
- Line chart showing last 30 days of data volume
- Displays:
  - Daily row count
  - Daily unique queries
- Uses spline interpolation for smooth lines
- Interactive hover shows exact values

## Technical Implementation

### New Files Created:
1. `src/data/metadata_queries.py` - Contains all metadata-specific BigQuery queries:
   - `get_data_overview()` - Main overview statistics
   - `get_data_freshness()` - Table freshness information
   - `get_daily_data_volume()` - Daily volume metrics
   - `get_data_quality_check()` - Data quality percentages

### Updated Files:
1. `src/data/__init__.py` - Added metadata functions:
   - `get_data_overview(domain)`
   - `get_data_freshness()`
   - `get_daily_data_volume(days_back, domain)`
   - `get_data_quality_check(domain)`

2. `app.py` - Added data overview section at the top

### Query Examples:
```sql
-- Data Overview Query
WITH data_stats AS (
    SELECT 
        COUNT(*) as total_rows,
        MIN(date) as earliest_date,
        MAX(date) as latest_date,
        COUNT(DISTINCT date) as days_with_data,
        COUNT(DISTINCT query) as unique_queries,
        COUNT(DISTINCT page) as unique_pages,
        COUNT(DISTINCT country) as unique_countries,
        SUM(clicks) as total_clicks,
        SUM(impressions) as total_impressions
    FROM search_console_data
    WHERE (page LIKE 'https://twelvetransfers.com%' OR page LIKE 'http://twelvetransfers.com%')
)
```

## Benefits

1. **Immediate Data Visibility**: Users can see at a glance:
   - How much data is available
   - When it was last updated
   - Overall data quality

2. **Data Freshness Monitoring**: 
   - Visual indicators for stale data
   - Easy identification of update issues

3. **Quality Assurance**:
   - Percentage of data quality issues
   - Helps identify data pipeline problems

4. **Domain-Specific**: All metrics respect the domain filter

## Usage

The data overview section appears automatically at the top of the dashboard and updates based on:
- Selected domain filter
- Real-time BigQuery data

No additional configuration is needed - the section loads automatically when the dashboard starts.

## Next Steps

Potential enhancements:
1. Add data ingestion history
2. Show data pipeline status
3. Add alerts for data quality thresholds
4. Include more detailed breakdowns by data source