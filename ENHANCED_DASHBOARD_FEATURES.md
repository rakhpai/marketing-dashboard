# Enhanced Marketing Dashboard Features

## Overview
The marketing dashboard has been significantly enhanced with better filtering capabilities, domain-specific data, and improved user experience.

## Key Enhancements

### 1. Domain-Specific Data Filtering
- All data queries now filter specifically for the selected domain (default: twelvetransfers.com)
- Option to select between:
  - twelvetransfers.com (default)
  - 12transfers.com
  - All domains
- Domain filter applies to all data sources:
  - Search Console performance metrics
  - Keyword data
  - Page performance
  - Device and country breakdowns
  - Conversion funnel data

### 2. Enhanced Date Filtering
- **Quick Date Presets:**
  - Last 7 days
  - Last 30 days (default)
  - Last 90 days
  - This month
  - Last month
  - Custom date range
- Visual date range indicator showing selected period
- Better UX with radio buttons for quick selection

### 3. Additional Filters
- **Device Type Filter:** Multi-select for DESKTOP, MOBILE, TABLET
- **Country Filter:** Text input for comma-separated country codes (e.g., US,GB,CA)
- **Page Type Filter:** Select specific page types (All pages, Homepage, Landing pages, etc.)
- **CTR Threshold:** Slider to filter by minimum Click-Through Rate (0-10%)
- **Position Threshold:** Slider to filter by maximum average position (1-100)

### 4. Data Export Capabilities
- Export data in multiple formats:
  - CSV
  - Excel
  - JSON
- Export button for keyword data with date-stamped filenames

### 5. Filter Summary Display
- Active filters are displayed at the top of the dashboard
- Clear indication of what filters are currently applied

### 6. Geographic Performance Section
- New section showing traffic breakdown by country
- Visual bar chart colored by CTR performance
- Country filter integration

### 7. Improved Query Structure
All BigQuery queries now include domain filtering:
```sql
WHERE ... AND (page LIKE 'https://{domain}%' OR page LIKE 'http://{domain}%')
```

## Technical Implementation

### Updated Files:
1. **app.py** - Enhanced with new filtering UI and logic
2. **src/data/queries.py** - All queries updated with domain parameter
3. **src/data/__init__.py** - All data functions updated to accept domain parameter

### New Features in Sidebar:
- Date range presets
- Domain selector
- Device type multi-select
- Country filter
- Page type selector
- CTR and position thresholds
- Export format selector

## Usage

The dashboard now provides much more granular control over the data being displayed:

1. **Select Domain:** Choose which domain to analyze
2. **Choose Date Range:** Use presets or custom dates
3. **Apply Filters:** Set device, country, CTR, and position filters
4. **Export Data:** Download filtered results in your preferred format

## Benefits

- **Domain-Specific Analysis:** Focus on twelvetransfers.com data only
- **Better Performance:** Queries are more targeted and faster
- **Enhanced UX:** Intuitive date presets and filter options
- **Data Export:** Easy data extraction for further analysis
- **Real-time Filtering:** See exactly what filters are active

The dashboard is now production-ready with comprehensive filtering capabilities specifically tailored for analyzing twelvetransfers.com SEO and marketing performance.