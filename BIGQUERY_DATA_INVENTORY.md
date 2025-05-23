# BigQuery Data Inventory

## Overview
This document provides a comprehensive inventory of all BigQuery datasets, tables, and views available for the Twelve Transfers marketing dashboard.

## Project Information
- **Project ID**: gtm-management-twelvetransfers
- **Service Account**: seo-data-integration@gtm-management-twelvetransfers.iam.gserviceaccount.com
- **Location**: US

## Datasets

### 1. seo_data
The main dataset containing Search Console data, keyword tracking, and SEO-related information.

### 2. analytics_399277695
Google Analytics 4 (GA4) data exported from the property.

---

## Tables & Views Inventory

### Dataset: seo_data

#### Tables (Physical Data)

##### 1. search_console_data
- **Type**: TABLE
- **Description**: Core Search Console data with clicks, impressions, CTR, and position metrics
- **Row Count**: 401,070 rows
- **Date Range**: 2024-02-19 to 2025-05-18
- **Schema**:
  - `id` (INTEGER) - Unique identifier
  - `date` (DATETIME) - Date of the data
  - `url` (STRING) - Page URL
  - `query` (STRING) - Search query
  - `country` (STRING) - Country code
  - `device` (STRING) - Device type (DESKTOP, MOBILE, TABLET)
  - `impressions` (INTEGER) - Number of impressions
  - `clicks` (INTEGER) - Number of clicks
  - `ctr` (FLOAT) - Click-through rate
  - `position` (FLOAT) - Average position
  - `created_at` (STRING) - Record creation timestamp
  - `year_month` (STRING) - Year-month for partitioning
  - `page_path` (STRING) - URL path component
  - `position_category` (STRING) - Position range category

##### 2. keyword_tracking
- **Type**: TABLE
- **Description**: Tracked keywords for position monitoring
- **Schema**: Contains keyword tracking configuration and history

##### 3. organic_results
- **Type**: TABLE
- **Description**: Organic search results from tracking tools
- **Schema**: Contains position data for tracked keywords

##### 4. related_questions
- **Type**: TABLE
- **Description**: People Also Ask and related questions data
- **Schema**: Contains related questions for keywords

#### Views (Virtual Tables)

##### 1. search_console_overview
- **Type**: VIEW
- **Description**: Daily aggregated Search Console metrics
- **Query**: Groups search_console_data by date with totals
- **Columns**:
  - `date` - Date
  - `total_clicks` - Sum of clicks
  - `total_impressions` - Sum of impressions
  - `avg_ctr` - Average CTR
  - `avg_position` - Average position

##### 2. keyword_performance
- **Type**: VIEW
- **Description**: Performance metrics grouped by keyword
- **Query**: Aggregates search_console_data by query
- **Columns**:
  - `query` - Search query
  - `total_clicks` - Total clicks
  - `total_impressions` - Total impressions
  - `avg_ctr` - Average CTR
  - `avg_position` - Average position

##### 3. page_performance
- **Type**: VIEW
- **Description**: Performance metrics grouped by page URL
- **Query**: Aggregates search_console_data by url
- **Columns**:
  - `url` - Page URL
  - `total_clicks` - Total clicks
  - `total_impressions` - Total impressions
  - `avg_ctr` - Average CTR
  - `avg_position` - Average position

##### 4. device_performance
- **Type**: VIEW
- **Description**: Performance metrics grouped by device type
- **Query**: Aggregates search_console_data by device
- **Columns**:
  - `device` - Device type
  - `total_clicks` - Total clicks
  - `total_impressions` - Total impressions
  - `avg_ctr` - Average CTR
  - `avg_position` - Average position

##### 5. country_performance
- **Type**: VIEW
- **Description**: Performance metrics grouped by country
- **Query**: Aggregates search_console_data by country
- **Columns**:
  - `country` - Country code
  - `total_clicks` - Total clicks
  - `total_impressions` - Total impressions
  - `avg_ctr` - Average CTR
  - `avg_position` - Average position

---

### Dataset: analytics_399277695 (GA4)

#### Tables (Physical Data)

##### Daily Event Tables
- **Pattern**: events_YYYYMMDD (e.g., events_20250518)
- **Type**: TABLE
- **Description**: Daily partitioned GA4 event data
- **Available Dates**: 2025-05-18 to 2025-05-21 (4 days)
- **Total Events**: 731 events
- **Schema**: Standard GA4 BigQuery export schema including:
  - Event parameters
  - User properties
  - Device information
  - Traffic source
  - Ecommerce data

##### Pseudonymous Users Tables
- **Pattern**: pseudonymous_users_YYYYMMDD
- **Type**: TABLE
- **Description**: Daily user data for GA4

---

## Data Quality Notes

### Search Console Data
- **Update Frequency**: Daily (appears to be updated regularly)
- **Data Completeness**: High - 401K+ rows covering over a year
- **Latest Data**: Up to May 18, 2025
- **Coverage**: Multiple countries, devices, and thousands of keywords

### GA4 Data
- **Update Frequency**: Daily exports
- **Data Completeness**: Limited - only 4 days of data
- **Latest Data**: Up to May 21, 2025
- **Note**: GA4 integration appears to be newly implemented

---

## Recommended Queries

### 1. Get Domain-Specific Data
```sql
SELECT * FROM `seo_data.search_console_data`
WHERE url LIKE 'https://twelvetransfers.com%'
```

### 2. Recent Performance Summary
```sql
SELECT * FROM `seo_data.search_console_overview`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
```

### 3. Top Keywords
```sql
SELECT * FROM `seo_data.keyword_performance`
LIMIT 100
```

### 4. GA4 Event Summary
```sql
SELECT 
  event_name,
  COUNT(*) as event_count
FROM `analytics_399277695.events_*`
GROUP BY event_name
ORDER BY event_count DESC
```

---

## Access Patterns

The marketing dashboard uses these tables/views through:
1. **Direct queries** to physical tables with custom filtering
2. **Pre-built views** for common aggregations
3. **Domain filtering** applied at query time
4. **Date range filtering** for performance optimization

---

## Future Considerations

1. **Data Retention**: Tables have expiration times set (60 days from creation)
2. **View Optimization**: Current views don't filter by domain
3. **GA4 Integration**: Only 4 days of data - needs monitoring
4. **Additional Views**: Consider creating domain-specific views for better performance