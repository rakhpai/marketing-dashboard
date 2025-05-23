import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Twelve Transfers Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dashboard title
st.title("Twelve Transfers Marketing Dashboard")

# Sidebar
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Date Range",
    [datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()]
)
channels = st.sidebar.multiselect(
    "Marketing Channels",
    ["Organic", "Paid Search", "Social Media", "Email", "Direct", "Referral"],
    default=["Organic", "Paid Search", "Social Media"]
)

# Generate sample data
def generate_data():
    dates = pd.date_range(
        start=date_range[0], 
        end=date_range[1] if len(date_range) > 1 else date_range[0],
        freq='D'
    )
    
    df_list = []
    
    for channel in channels:
        base_traffic = np.random.randint(100, 1000)
        base_conversion = np.random.uniform(0.01, 0.05)
        
        for date in dates:
            traffic = base_traffic + np.random.randint(-100, 100)
            conversion_rate = base_conversion + np.random.uniform(-0.01, 0.01)
            conversions = int(traffic * conversion_rate)
            revenue = conversions * np.random.randint(50, 200)
            
            df_list.append({
                'Date': date,
                'Channel': channel,
                'Traffic': traffic,
                'Conversions': conversions,
                'Revenue': revenue,
                'Conversion Rate': conversion_rate
            })
    
    return pd.DataFrame(df_list)

# Generate data
df = generate_data()

# Main content
st.write("### Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Traffic",
        f"{df['Traffic'].sum():,}",
        f"{int(df['Traffic'].sum() * 0.1):+,}"
    )

with col2:
    st.metric(
        "Total Conversions",
        f"{df['Conversions'].sum():,}",
        f"{int(df['Conversions'].sum() * 0.15):+,}"
    )

with col3:
    st.metric(
        "Total Revenue",
        f"£{int(df['Revenue'].sum()):,}",
        f"{int(df['Revenue'].sum() * 0.12):+,}"
    )

with col4:
    avg_conv_rate = df['Conversions'].sum() / df['Traffic'].sum()
    st.metric(
        "Avg. Conversion Rate",
        f"{avg_conv_rate:.2%}",
        f"{0.005:.2%}"
    )

st.write("### Traffic by Channel")
# Group by channel and calculate sums
channel_metrics = df.groupby('Channel').agg({
    'Traffic': 'sum',
    'Conversions': 'sum',
    'Revenue': 'sum'
}).reset_index()

# Calculate conversion rate
channel_metrics['Conversion Rate'] = channel_metrics['Conversions'] / channel_metrics['Traffic']

# Display as a bar chart
chart = alt.Chart(channel_metrics).mark_bar().encode(
    x=alt.X('Channel:N', sort='-y'),
    y=alt.Y('Traffic:Q'),
    color=alt.Color('Channel:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Channel', 'Traffic', 'Conversions', 'Revenue', alt.Tooltip('Conversion Rate:Q', format='.2%')]
).properties(
    height=400
)
st.altair_chart(chart, use_container_width=True)

st.write("### Daily Traffic Trends")
# Group by date and calculate sums
daily_metrics = df.groupby(['Date', 'Channel']).agg({
    'Traffic': 'sum'
}).reset_index()

# Create line chart
line_chart = alt.Chart(daily_metrics).mark_line().encode(
    x='Date:T',
    y='Traffic:Q',
    color='Channel:N',
    tooltip=['Date', 'Channel', 'Traffic']
).properties(
    height=400
)
st.altair_chart(line_chart, use_container_width=True)

st.write("### Revenue by Channel")
revenue_chart = alt.Chart(channel_metrics).mark_bar().encode(
    x=alt.X('Channel:N', sort='-y'),
    y=alt.Y('Revenue:Q'),
    color=alt.Color('Channel:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Channel', 'Revenue', 'Conversions']
).properties(
    height=400
)
st.altair_chart(revenue_chart, use_container_width=True)

st.write("### Detailed Metrics Table")
st.dataframe(
    channel_metrics.style.format({
        'Traffic': '{:,.0f}',
        'Conversions': '{:,.0f}',
        'Revenue': '£{:,.2f}',
        'Conversion Rate': '{:.2%}'
    }),
    use_container_width=True
)

# Footer
st.write("---")
st.write("Dashboard last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))