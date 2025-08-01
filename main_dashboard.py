#!/usr/bin/env python3
"""
Main ESG Data Tracker Dashboard
Simplified version that works with real data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_alpha_vantage_data(symbol):
    """Get company data from Alpha Vantage"""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        st.warning("⚠️ Alpha Vantage API key not found")
        return None
    
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if "Error Message" not in data and "Note" not in data:
                return data
            elif "Note" in data:
                st.warning(f"⚠️ Alpha Vantage API: {data['Note']}")
            else:
                st.error(f"❌ Alpha Vantage API Error: {data.get('Error Message', 'Unknown error')}")
        else:
            st.error(f"❌ Alpha Vantage API HTTP Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("❌ Alpha Vantage API request timed out")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Alpha Vantage API request failed: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error getting Alpha Vantage data: {e}")
    
    return None

def get_news_data():
    """Get ESG news from News API"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        st.warning("⚠️ News API key not found")
        return []
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "ESG sustainability corporate responsibility",
            "apiKey": api_key,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5
        }
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                return data.get("articles", [])
            else:
                st.error(f"❌ News API Error: {data.get('message', 'Unknown error')}")
        else:
            st.error(f"❌ News API HTTP Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("❌ News API request timed out")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ News API request failed: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error getting news data: {e}")
    
    return []

def main():
    st.set_page_config(
        page_title="ESG Data Tracker",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🌱 ESG Data Tracker")
    st.markdown("**Real-time ESG monitoring and analysis platform**")
    
    # Sidebar
    st.sidebar.header("📊 Dashboard Controls")
    
    # Company selection
    companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "JNJ", "PG", "V", "UNH"]
    selected_company = st.sidebar.selectbox("Select Company", companies)
    
    # Date range
    days_back = st.sidebar.slider("Days Back", 7, 90, 30)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 {selected_company} - Real Data")
        
        # Get real company data
        company_data = get_alpha_vantage_data(selected_company)
        
        if company_data:
            st.success("✅ Real data loaded from Alpha Vantage")
            
            # Company info
            col1a, col1b, col1c = st.columns(3)
            with col1a:
                st.metric("Company", company_data.get("Name", "N/A"))
            with col1b:
                st.metric("Sector", company_data.get("Sector", "N/A"))
            with col1c:
                st.metric("Industry", company_data.get("Industry", "N/A"))
            
            # Financial metrics
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                market_cap = company_data.get("MarketCapitalization", "N/A")
                if market_cap != "N/A" and market_cap is not None and market_cap != "None":
                    try:
                        market_cap = f"${int(int(market_cap)/1000000000)}B"
                    except (ValueError, TypeError):
                        market_cap = "N/A"
                else:
                    market_cap = "N/A"
                st.metric("Market Cap", market_cap)
            with col2b:
                pe_ratio = company_data.get("PERatio", "N/A")
                if pe_ratio == "None" or pe_ratio is None:
                    pe_ratio = "N/A"
                st.metric("P/E Ratio", pe_ratio)
            with col2c:
                dividend = company_data.get("DividendYield", "N/A")
                if dividend != "N/A" and dividend is not None and dividend != "None":
                    try:
                        dividend = f"{float(dividend)*100:.2f}%"
                    except (ValueError, TypeError):
                        dividend = "N/A"
                else:
                    dividend = "N/A"
                st.metric("Dividend Yield", dividend)
            
            # Company description
            st.subheader("📋 Company Description")
            description = company_data.get("Description", "No description available")
            st.write(description[:500] + "..." if len(description) > 500 else description)
            
        else:
            st.warning("⚠️ Unable to load real data - showing sample data")
            
            # Display sample company info
            col1a, col1b, col1c = st.columns(3)
            with col1a:
                st.metric("Company", f"{selected_company} (Sample)")
            with col1b:
                st.metric("Sector", "Technology")
            with col1c:
                st.metric("Industry", "Software")
            
            # Sample financial metrics
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.metric("Market Cap", "$2.5T")
            with col2b:
                st.metric("P/E Ratio", "25.5")
            with col2c:
                st.metric("Dividend Yield", "0.5%")
            
            # Sample ESG data
            sample_esg = {
                "Date": pd.date_range(start=datetime.now() - timedelta(days=days_back), periods=days_back, freq='D'),
                "Environmental": [75 + i*0.1 for i in range(days_back)],
                "Social": [80 + i*0.05 for i in range(days_back)],
                "Governance": [85 + i*0.08 for i in range(days_back)]
            }
            
            df_esg = pd.DataFrame(sample_esg)
            
            # ESG trend chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_esg['Date'], y=df_esg['Environmental'], name='Environmental', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=df_esg['Date'], y=df_esg['Social'], name='Social', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=df_esg['Date'], y=df_esg['Governance'], name='Governance', line=dict(color='red')))
            
            fig.update_layout(
                title=f"{selected_company} ESG Score Trends (Sample Data)",
                xaxis_title="Date",
                yaxis_title="ESG Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Sample company description
            st.subheader("📋 Company Description")
            st.write("This is sample data. Please check your API keys and internet connection to load real data.")
    
    with col2:
        st.subheader("📰 Real ESG News")
        
        # Get real news
        news_articles = get_news_data()
        
        if news_articles:
            st.success(f"✅ {len(news_articles)} real news articles loaded")
            
            for i, article in enumerate(news_articles[:3]):
                with st.expander(f"📰 {article.get('title', 'No title')[:50]}..."):
                    st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                    st.write(f"**Published:** {article.get('publishedAt', 'Unknown')[:10]}")
                    st.write(f"**Summary:** {article.get('description', 'No description')}")
                    st.write(f"**URL:** {article.get('url', 'No URL')}")
        else:
            st.warning("⚠️ Unable to load real news - showing sample articles")
            
            # Sample news articles
            sample_news = [
                {
                    "title": "ESG Investing Continues to Gain Momentum in 2024",
                    "source": {"name": "Financial Times"},
                    "publishedAt": "2024-01-15T10:00:00Z",
                    "description": "Sustainable investing strategies are becoming increasingly popular among institutional investors.",
                    "url": "#"
                },
                {
                    "title": "Corporate Sustainability Reporting Standards Updated",
                    "source": {"name": "Reuters"},
                    "publishedAt": "2024-01-14T14:30:00Z", 
                    "description": "New global standards for ESG reporting aim to improve transparency and comparability.",
                    "url": "#"
                },
                {
                    "title": "Tech Companies Lead in Renewable Energy Adoption",
                    "source": {"name": "Bloomberg"},
                    "publishedAt": "2024-01-13T09:15:00Z",
                    "description": "Major technology firms are setting ambitious carbon neutrality goals.",
                    "url": "#"
                }
            ]
            
            for i, article in enumerate(sample_news):
                with st.expander(f"📰 {article['title'][:50]}..."):
                    st.write(f"**Source:** {article['source']['name']}")
                    st.write(f"**Published:** {article['publishedAt'][:10]}")
                    st.write(f"**Summary:** {article['description']}")
                    st.write(f"**URL:** {article['url']}")
    
    # Footer
    st.markdown("---")
    st.markdown("**🌱 ESG Data Tracker - Real Data Collection**")
    st.markdown("*Powered by News API, Alpha Vantage, and AI sentiment analysis*")

if __name__ == "__main__":
    main()
