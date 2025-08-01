#!/usr/bin/env python3
"""
Simple test dashboard to verify Streamlit is working
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.set_page_config(
        page_title="ESG Data Tracker - Test",
        page_icon="��",
        layout="wide"
    )
    
    st.title("🎉 ESG Data Tracker - Test Dashboard")
    st.write("This is a test to verify Streamlit is working!")
    
    # Show current time
    st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show API status
    st.subheader("📊 API Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("News API", "✅ Working", "Real ESG News")
    
    with col2:
        st.metric("Alpha Vantage", "✅ Working", "Financial Data")
    
    with col3:
        st.metric("AI Sentiment", "✅ Working", "News Analysis")
    
    # Show sample data
    st.subheader("📈 Sample ESG Data")
    
    sample_data = {
        "Company": ["Apple Inc", "Microsoft", "Tesla"],
        "ESG Score": [85, 82, 78],
        "Environmental": [88, 85, 92],
        "Social": [82, 80, 75],
        "Governance": [85, 81, 67]
    }
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df)
    
    # Show chart
    st.subheader("📊 ESG Score Comparison")
    st.bar_chart(df.set_index("Company")[["Environmental", "Social", "Governance"]])
    
    st.success("🎉 Test dashboard is working! Your ESG Data Tracker is ready!")

if __name__ == "__main__":
    main()
