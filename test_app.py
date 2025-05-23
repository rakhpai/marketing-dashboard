import streamlit as st
import pandas as pd
import numpy as np

st.title("TEST STREAMLIT APP - Marketing Dashboard")
st.write("This is a test to verify Streamlit is working properly")

# Simple chart
data = pd.DataFrame({
    'x': range(10),
    'y': np.random.randn(10)
})

st.line_chart(data)
st.write("If you can see this text and the chart above, Streamlit is working!")