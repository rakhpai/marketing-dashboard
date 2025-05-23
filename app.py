import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import altair as alt
import plotly.express as px
import logging

# Import our custom modules
from src.data import (
    get_search_performance_data, 
    get_keyword_data,
    get_page_performance_data,
    get_traffic_by_device,
    get_traffic_by_country,
    get_conversion_funnel_data,
    get_weekly_performance_summary,
    get_query_category_performance,
    test_bigquery_connection,
    get_data_overview,
    get_daily_data_volume,
    get_search_console_daily_trend,
    get_top_keywords_from_view,
    get_top_pages_from_view,
    get_tracked_keywords_with_positions,
    get_ga4_event_summary,
    get_ga4_daily_users,
    get_position_distribution
)
from src.components.enhanced_components import (
    load_enhanced_css,
    create_enhanced_metric_card,
    create_enhanced_trend_chart,
    create_comparison_chart,
    create_donut_chart,
    create_multi_metric_row,
    create_section_header,
    create_info_box
)
from src.components.charts import (
    create_conversion_funnel,
    create_time_series_comparison,
    create_keyword_cloud,
    create_performance_gauge
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Twelve Transfers Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
load_enhanced_css()

# Dashboard title
st.title("🚀 Twelve Transfers Marketing Analytics Dashboard")

# Test BigQuery connection
@st.cache_data(ttl=3600)
def test_connection():
    return test_bigquery_connection()

# Sidebar
st.sidebar.header("Filters & Settings")

# Enhanced Date Range Selector with Presets
st.sidebar.subheader("📅 Date Range")

# Date preset buttons
date_preset = st.sidebar.radio(
    "Quick Select",
    ["Last 7 days", "Last 30 days", "Last 90 days", "This month", "Last month", "Custom"],
    index=1
)

# Calculate dates based on preset
today = datetime.date.today()
if date_preset == "Last 7 days":
    start_date = today - timedelta(days=7)
    end_date = today
elif date_preset == "Last 30 days":
    start_date = today - timedelta(days=30)
    end_date = today
elif date_preset == "Last 90 days":
    start_date = today - timedelta(days=90)
    end_date = today
elif date_preset == "This month":
    start_date = today.replace(day=1)
    end_date = today
elif date_preset == "Last month":
    last_month = today.replace(day=1) - timedelta(days=1)
    start_date = last_month.replace(day=1)
    end_date = last_month
else:  # Custom
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", today - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", today)

# Display selected date range
st.sidebar.info(f"📊 Showing data from **{start_date}** to **{end_date}**")

# Domain Filter
st.sidebar.subheader("🌐 Domain")
domain = st.sidebar.selectbox(
    "Select Domain",
    ["All domains", "twelvetransfers.com", "12transfers.com"],
    index=0  # Default to "All domains"
)

# Additional Filters
st.sidebar.subheader("🔧 Additional Filters")

# Device filter
device_filter = st.sidebar.multiselect(
    "Device Type",
    ["DESKTOP", "MOBILE", "TABLET"],
    default=["DESKTOP", "MOBILE", "TABLET"]
)

# Country filter
country_filter = st.sidebar.text_input(
    "Country (comma-separated codes)",
    placeholder="e.g., US,GB,CA",
    help="Leave empty for all countries"
)

# Page type filter
page_type_filter = st.sidebar.selectbox(
    "Page Type",
    ["All pages", "Homepage only", "Landing pages", "Blog posts", "Service pages"]
)

# CTR threshold
ctr_threshold = st.sidebar.slider(
    "Minimum CTR %",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.1,
    help="Filter results by minimum Click-Through Rate"
)

# Position threshold
position_threshold = st.sidebar.slider(
    "Maximum Average Position",
    min_value=1,
    max_value=100,
    value=100,
    help="Filter results by maximum average position"
)

# Auto-refresh option
st.sidebar.subheader("⚙️ Settings")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
if auto_refresh:
    st.experimental_rerun()

# Data source toggle
use_real_data = st.sidebar.checkbox("Use Real Data", value=True)

# Test connection button
if st.sidebar.button("🔍 Test Data Connection"):
    with st.spinner("Testing connection..."):
        if test_connection():
            st.sidebar.success("✅ BigQuery connection successful!")
        else:
            st.sidebar.error("❌ BigQuery connection failed!")

# Export options
st.sidebar.subheader("📥 Export Data")
export_format = st.sidebar.selectbox(
    "Export Format",
    ["CSV", "Excel", "JSON"]
)

# Generate sample data (fallback)
def generate_sample_data():
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    df_list = []
    channels = ["Organic", "Paid Search", "Social Media", "Email", "Direct", "Referral"]
    
    for channel in channels:
        base_traffic = np.random.randint(100, 1000)
        base_conversion = np.random.uniform(0.01, 0.05)
        
        for date in dates:
            traffic = base_traffic + np.random.randint(-100, 100)
            conversion_rate = base_conversion + np.random.uniform(-0.01, 0.01)
            conversions = int(traffic * conversion_rate)
            revenue = conversions * np.random.randint(50, 200)
            
            df_list.append({
                'date': date,
                'channel': channel,
                'total_clicks': traffic,
                'total_impressions': traffic * 20,
                'conversions': conversions,
                'revenue': revenue,
                'avg_ctr': conversion_rate,
                'avg_position': np.random.uniform(1, 10)
            })
    
    return pd.DataFrame(df_list)

# Load data with caching and domain filtering
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_search_data(start_date, end_date, domain_filter):
    try:
        if use_real_data:
            # Use domain filter - if "All domains" is selected, use None
            selected_domain = None if domain_filter == "All domains" else domain_filter
            
            data = get_search_performance_data(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                domain=selected_domain
            )
            if data.empty:
                st.warning("No real data available, using sample data instead.")
                return generate_sample_data()
            return data
        else:
            return generate_sample_data()
    except Exception as e:
        logger.error(f"Error loading search data: {e}")
        st.error(f"Error loading data: {e}")
        return generate_sample_data()

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_keyword_data(domain_filter):
    try:
        if use_real_data:
            selected_domain = None if domain_filter == "All domains" else domain_filter
            return get_keyword_data(limit=50, domain=selected_domain)
        else:
            # Generate sample keyword data
            keywords = ['miami transfer', 'airport taxi', 'twelve transfers', 'book taxi online', 
                       'airport shuttle', 'private transfer', 'taxi booking', 'transfer service']
            data = []
            for kw in keywords:
                data.append({
                    'keyword': kw,
                    'total_clicks': np.random.randint(100, 5000),
                    'total_impressions': np.random.randint(1000, 50000),
                    'avg_ctr_percentage': np.random.uniform(1, 5),
                    'avg_position': np.random.uniform(1, 20)
                })
            return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error loading keyword data: {e}")
        return pd.DataFrame()

# Main content
try:
    # Data Overview Section - ALWAYS AT THE TOP
    create_section_header("🗃️ BigQuery Data Overview")
    
    # Get data overview
    data_overview = get_data_overview(None)
    
    if data_overview:
        # Display data overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Rows",
                f"{data_overview.get('total_rows', 0):,}",
                help="Total number of rows in search console data"
            )
            st.metric(
                "Unique Queries",
                f"{data_overview.get('unique_queries', 0):,}",
                help="Number of unique search queries"
            )
        
        with col2:
            earliest = data_overview.get('earliest_date')
            latest = data_overview.get('latest_date')
            if earliest and latest:
                st.metric(
                    "Data Range",
                    f"{data_overview.get('days_with_data', 0)} days",
                    help=f"From {earliest} to {latest}"
                )
            st.metric(
                "Unique Pages",
                f"{data_overview.get('unique_pages', 0):,}",
                help="Number of unique pages with data"
            )
        
        with col3:
            last_update = data_overview.get('last_data_date')
            days_since = data_overview.get('days_since_update', 0)
            if last_update:
                st.metric(
                    "Last Data Update",
                    f"{last_update}",
                    f"{days_since} days ago" if days_since > 0 else "Today",
                    delta_color="inverse" if days_since > 3 else "normal"
                )
            st.metric(
                "Total Clicks",
                f"{data_overview.get('total_clicks', 0):,}",
                help="Total clicks across all data"
            )
        
        with col4:
            st.metric(
                "Total Impressions", 
                f"{data_overview.get('total_impressions', 0):,}",
                help="Total impressions across all data"
            )
            st.metric(
                "Countries",
                f"{data_overview.get('unique_countries', 0):,}",
                help="Number of countries in the data"
            )
    
    # Daily Data Volume Chart - Real Search Console Data
    create_section_header("📈 Daily Search Console Activity")
    
    # Get 60 days to show more data points since data is sparse
    volume_data = get_daily_data_volume(60, None)
    if not volume_data.empty:
        # Create a more informative chart
        col1, col2 = st.columns([3, 1])
        
        with col1:
            fig = px.bar(
                volume_data,
                x='date',
                y='total_clicks',
                title="Daily Clicks from Search Console (Last 60 Days)",
                labels={'total_clicks': 'Total Clicks', 'date': 'Date'},
                color='total_impressions',
                color_continuous_scale='Blues',
                hover_data={
                    'row_count': ':,.0f',
                    'unique_queries': ':,.0f',
                    'unique_pages': ':,.0f',
                    'total_impressions': ':,.0f'
                }
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                hovermode='x unified',
                xaxis_tickformat='%Y-%m-%d'
            )
            fig.update_traces(
                hovertemplate='<b>Date:</b> %{x}<br>' +
                             '<b>Clicks:</b> %{y:,.0f}<br>' +
                             '<b>Impressions:</b> %{customdata[3]:,.0f}<br>' +
                             '<b>Queries:</b> %{customdata[1]:,.0f}<br>' +
                             '<b>Pages:</b> %{customdata[2]:,.0f}<br>' +
                             '<b>Rows:</b> %{customdata[0]:,.0f}<extra></extra>'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Summary statistics
            st.metric(
                "Days with Data",
                f"{len(volume_data)}",
                help="Number of days with search console data in the last 60 days"
            )
            st.metric(
                "Total Clicks",
                f"{volume_data['total_clicks'].sum():,}",
                help="Sum of all clicks in the displayed period"
            )
            st.metric(
                "Avg Daily Clicks",
                f"{volume_data['total_clicks'].mean():.1f}",
                help="Average clicks per day (when data exists)"
            )
            st.metric(
                "Total Queries",
                f"{volume_data['unique_queries'].sum():,}",
                help="Total unique queries across all days"
            )
    else:
        st.info("No daily data available for the selected period")
    
    st.divider()
    
    # Load data (domain filter is ignored in simplified queries)
    search_data = load_search_data(start_date, end_date, None)
    keyword_data = load_keyword_data(None)
    
    # Apply additional filters if data is loaded
    if not search_data.empty and 'avg_ctr' in search_data.columns:
        # Apply CTR filter
        if ctr_threshold > 0:
            search_data = search_data[search_data['avg_ctr'] * 100 >= ctr_threshold]
        
        # Apply position filter
        if 'avg_position' in search_data.columns:
            search_data = search_data[search_data['avg_position'] <= position_threshold]
    
    # Filter summary
    active_filters = []
    if domain != "All domains":
        active_filters.append(f"Domain: {domain}")
    if ctr_threshold > 0:
        active_filters.append(f"CTR ≥ {ctr_threshold}%")
    if position_threshold < 100:
        active_filters.append(f"Position ≤ {position_threshold}")
    if country_filter:
        active_filters.append(f"Countries: {country_filter}")
    if len(device_filter) < 3:
        active_filters.append(f"Devices: {', '.join(device_filter)}")
    
    if active_filters:
        st.info(f"🔍 Active filters: {' • '.join(active_filters)}")
    
    # Overview Section
    create_section_header("📊 Overview Metrics")
    
    if not search_data.empty:
        # Calculate metrics
        total_clicks = search_data['total_clicks'].sum()
        total_impressions = search_data['total_impressions'].sum()
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_position = search_data['avg_position'].mean()
        
        # Calculate week-over-week changes
        if len(search_data) > 7:
            last_week = search_data.tail(7)['total_clicks'].sum()
            prev_week = search_data.iloc[-14:-7]['total_clicks'].sum() if len(search_data) > 14 else last_week
            click_change = ((last_week - prev_week) / prev_week * 100) if prev_week > 0 else 0
        else:
            click_change = 0
        
        # Display metrics
        metrics = [
            {
                'title': 'Total Clicks',
                'value': total_clicks,
                'delta': click_change,
                'prefix': '',
                'suffix': ''
            },
            {
                'title': 'Total Impressions',
                'value': total_impressions,
                'delta': None,
                'prefix': '',
                'suffix': ''
            },
            {
                'title': 'Average CTR',
                'value': f"{avg_ctr:.2f}",
                'delta': None,
                'prefix': '',
                'suffix': '%'
            },
            {
                'title': 'Average Position',
                'value': f"{avg_position:.1f}",
                'delta': None,
                'prefix': '',
                'suffix': ''
            }
        ]
        
        create_multi_metric_row(metrics)
    
    # Traffic Trends
    create_section_header("📈 Traffic Trends")
    
    if not search_data.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Time series chart
            fig = create_enhanced_trend_chart(
                search_data,
                "Daily Click Trends",
                "date",
                "total_clicks",
                show_average=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Get device breakdown
            device_data = get_traffic_by_device(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                domain=None
            )
            
            # Apply device filter
            if not device_data.empty and device_filter:
                device_data = device_data[device_data['device'].isin(device_filter)]
            
            if not device_data.empty:
                fig = create_donut_chart(
                    device_data['device'].tolist(),
                    device_data['total_clicks'].tolist(),
                    "Traffic by Device"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Keyword Performance
    create_section_header("🔍 Keyword Performance")
    
    if not keyword_data.empty:
        # Apply filters to keyword data
        if ctr_threshold > 0:
            keyword_data = keyword_data[keyword_data['avg_ctr_percentage'] >= ctr_threshold]
        if position_threshold < 100:
            keyword_data = keyword_data[keyword_data['avg_position'] <= position_threshold]
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Top keywords table
            st.subheader("Top Performing Keywords")
            
            # Add export button
            if st.button("📥 Export Keywords"):
                if export_format == "CSV":
                    csv = keyword_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"keywords_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
            
            st.dataframe(
                keyword_data.head(10).style.format({
                    'total_clicks': '{:,.0f}',
                    'total_impressions': '{:,.0f}',
                    'avg_ctr_percentage': '{:.2f}%',
                    'avg_position': '{:.1f}'
                }),
                use_container_width=True
            )
        
        with col2:
            # Keyword cloud
            if len(keyword_data) > 0:
                fig = create_keyword_cloud(
                    keyword_data.head(20),
                    'keyword',
                    'total_clicks',
                    "Top Keywords by Clicks"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Geographic Performance
    create_section_header("🌍 Geographic Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get country data
        country_data = get_traffic_by_country(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            limit=10,
            domain=None
        )
        
        # Apply country filter if specified
        if country_filter and not country_data.empty:
            countries = [c.strip().upper() for c in country_filter.split(',')]
            country_data = country_data[country_data['country'].isin(countries)]
        
        if not country_data.empty:
            st.subheader("Top Countries by Traffic")
            st.dataframe(
                country_data.style.format({
                    'total_clicks': '{:,.0f}',
                    'total_impressions': '{:,.0f}',
                    'avg_ctr_percentage': '{:.2f}%',
                    'avg_position': '{:.1f}'
                }),
                use_container_width=True
            )
    
    with col2:
        if not country_data.empty:
            fig = px.bar(
                country_data.head(10),
                x='total_clicks',
                y='country',
                orientation='h',
                title="Clicks by Country",
                color='avg_ctr_percentage',
                color_continuous_scale='Blues',
                labels={'total_clicks': 'Total Clicks', 'country': 'Country'}
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Conversion Funnel
    create_section_header("🎯 Conversion Funnel")
    
    # Get funnel data
    funnel_data = get_conversion_funnel_data(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        domain=None
    )
    
    if funnel_data:
        fig = create_conversion_funnel(funnel_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # Query Category Performance
    create_section_header("📊 Performance by Query Type")
    
    query_category_data = get_query_category_performance(domain=None)
    
    if not query_category_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Branded vs Non-branded comparison
            fig = create_comparison_chart(
                query_category_data,
                "Branded vs Non-Branded Queries",
                ['query_type'],
                ['total_clicks', 'total_impressions'],
                chart_type='bar'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance metrics
            for _, row in query_category_data.iterrows():
                st.metric(
                    f"{row['query_type']} Queries",
                    f"{row['total_clicks']:,} clicks",
                    f"CTR: {row['avg_ctr_percentage']:.2f}%"
                )
    
    # Keyword Position Tracking
    create_section_header("📍 Keyword Position Tracking")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tracked keywords with positions
        tracked_keywords = get_tracked_keywords_with_positions(50)
        if not tracked_keywords.empty:
            st.subheader("Top Tracked Keywords by Position")
            st.dataframe(
                tracked_keywords[['keyword', 'position', 'search_engine', 'title']].style.format({
                    'position': '{:.0f}'
                }),
                use_container_width=True,
                height=400
            )
    
    with col2:
        # Position distribution
        position_dist = get_position_distribution()
        if not position_dist.empty:
            st.subheader("Position Distribution")
            fig = px.pie(
                position_dist,
                values='keyword_count',
                names='position_range',
                title="Keywords by Position Range",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Search Console Daily Trends from View
    create_section_header("📈 Search Console Daily Trends (View)")
    
    daily_trend = get_search_console_daily_trend(30)
    if not daily_trend.empty:
        # Create tabs for different metrics
        tab1, tab2, tab3 = st.tabs(["Clicks & Impressions", "CTR Trend", "Position Trend"])
        
        with tab1:
            fig = px.line(
                daily_trend,
                x='date',
                y=['total_clicks', 'total_impressions'],
                title="Daily Clicks and Impressions",
                labels={'value': 'Count', 'variable': 'Metric'},
                line_shape='spline'
            )
            fig.update_layout(
                height=400,
                hovermode='x unified',
                yaxis2=dict(overlaying='y', side='right')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.area(
                daily_trend,
                x='date',
                y='ctr_percentage',
                title="Click-Through Rate Trend",
                labels={'ctr_percentage': 'CTR (%)'},
                line_shape='spline'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = px.line(
                daily_trend,
                x='date',
                y='avg_position',
                title="Average Position Trend (Lower is Better)",
                labels={'avg_position': 'Average Position'},
                line_shape='spline'
            )
            fig.update_yaxis(autorange='reversed')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # GA4 Analytics Section
    create_section_header("📊 Google Analytics 4 Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GA4 Daily Users
        ga4_users = get_ga4_daily_users(7)
        if not ga4_users.empty:
            st.subheader("Daily Active Users")
            fig = px.bar(
                ga4_users,
                x='date',
                y='unique_users',
                title="Daily Active Users (Last 7 Days)",
                labels={'unique_users': 'Unique Users', 'date': 'Date'},
                text='unique_users'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # GA4 Event Summary
        ga4_events = get_ga4_event_summary(7)
        if not ga4_events.empty:
            st.subheader("Top Events (Last 7 Days)")
            st.dataframe(
                ga4_events[['event_name', 'event_count', 'unique_users']].head(10).style.format({
                    'event_count': '{:,.0f}',
                    'unique_users': '{:,.0f}'
                }),
                use_container_width=True,
                height=350
            )
    
    # Top Pages from View
    create_section_header("📄 Top Performing Pages (from View)")
    
    top_pages = get_top_pages_from_view(20)
    if not top_pages.empty:
        # Clean URLs for display
        top_pages['clean_url'] = top_pages['url'].apply(
            lambda x: x.replace('https://twelvetransfers.com', '').replace('https://www.twelvetransfers.com', '')
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            fig = px.bar(
                top_pages.head(10),
                x='total_clicks',
                y='clean_url',
                orientation='h',
                title="Top 10 Pages by Clicks",
                labels={'total_clicks': 'Total Clicks', 'clean_url': 'Page'},
                color='ctr_percentage',
                color_continuous_scale='Viridis',
                text='total_clicks'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                coloraxis_colorbar=dict(title="CTR %")
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Summary metrics
            st.metric("Total Pages", f"{len(top_pages):,}")
            st.metric(
                "Avg CTR",
                f"{top_pages['ctr_percentage'].mean():.2f}%"
            )
            st.metric(
                "Avg Position",
                f"{top_pages['avg_position'].mean():.1f}"
            )
    
    # Info box
    create_info_box(
        "Data Source",
        f"{'Real-time BigQuery data' if use_real_data else 'Sample data'} for {domain} from {start_date} to {end_date}"
    )
    
except Exception as e:
    logger.error(f"Error in main dashboard: {e}")
    st.error(f"An error occurred while loading the dashboard: {str(e)}")
    st.info("Please check your data connection and try again.")

# Footer
st.write("---")
st.write("Dashboard last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))