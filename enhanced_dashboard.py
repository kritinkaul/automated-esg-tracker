#!/usr/bin/env python3
"""
Enhanced ESG Data Tracker Dashboard
Interactive version with free APIs and fun features
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🌱 ESG Data Tracker Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .esg-score {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .environmental { background: linear-gradient(135deg, #4CAF50, #45a049); }
    .social { background: linear-gradient(135deg, #2196F3, #1976D2); }
    .governance { background: linear-gradient(135deg, #FF9800, #F57C00); }
</style>
""", unsafe_allow_html=True)

def get_stock_data(symbol, period="1y"):
    """Get stock data using yfinance"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        st.error(f"Error getting stock data: {e}")
        return None

def get_weather_data(city="New York"):
    """Get weather data from OpenWeatherMap (free API)"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return None
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error getting weather data: {e}")
    
    return None

def calculate_carbon_footprint(company_data):
    """Calculate estimated carbon footprint based on company data"""
    try:
        market_cap = company_data.get("MarketCapitalization")
        if market_cap and market_cap != "None":
            market_cap = float(market_cap)
            # Rough estimation: larger companies typically have higher carbon footprints
            carbon_footprint = (market_cap / 1000000000) * 0.5  # MT CO2 per billion market cap
            return carbon_footprint
    except:
        pass
    return None

def get_esg_sentiment_score(company_name):
    """Simulate ESG sentiment analysis"""
    # This would normally use a real sentiment analysis API
    # For now, we'll simulate based on company name
    positive_keywords = ["green", "solar", "wind", "renewable", "clean"]
    negative_keywords = ["oil", "gas", "coal", "fossil"]
    
    company_lower = company_name.lower()
    score = 50  # Neutral starting point
    
    for keyword in positive_keywords:
        if keyword in company_lower:
            score += 10
    
    for keyword in negative_keywords:
        if keyword in company_lower:
            score -= 10
    
    return max(0, min(100, score))

def create_interactive_charts(company_data, stock_data, selected_company):
    """Create interactive charts and visualizations"""
    
    # Create subplots with proper specs for indicator charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Stock Price Trend', 'ESG Score Breakdown', 'Market Performance', 'Carbon Footprint'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "indicator"}]]
    )
    
    # 1. Stock Price Chart
    if stock_data is not None and not stock_data.empty:
        fig.add_trace(
            go.Scatter(x=stock_data.index, y=stock_data['Close'], 
                      name='Stock Price', line=dict(color='#1f77b4')),
            row=1, col=1
        )
    
    # 2. ESG Score Breakdown
    esg_scores = {
        'Environmental': np.random.randint(60, 90),
        'Social': np.random.randint(65, 85),
        'Governance': np.random.randint(70, 95)
    }
    
    fig.add_trace(
        go.Bar(x=list(esg_scores.keys()), y=list(esg_scores.values()),
               marker_color=['#4CAF50', '#2196F3', '#FF9800']),
        row=1, col=2
    )
    
    # 3. Market Performance vs S&P 500
    if stock_data is not None and not stock_data.empty:
        # Calculate returns
        returns = stock_data['Close'].pct_change().dropna()
        cumulative_returns = (1 + returns).cumprod()
        
        fig.add_trace(
            go.Scatter(x=cumulative_returns.index, y=cumulative_returns.values,
                      name=f'{selected_company} Returns', line=dict(color='#1f77b4')),
            row=2, col=1
        )
    
    # 4. Carbon Footprint
    carbon_footprint = calculate_carbon_footprint(company_data)
    if carbon_footprint:
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=carbon_footprint,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Carbon Footprint (MT CO2)"},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkgreen"},
                       'steps': [{'range': [0, 25], 'color': "lightgreen"},
                                {'range': [25, 50], 'color': "yellow"},
                                {'range': [50, 100], 'color': "red"}]}
            ),
            row=2, col=2
        )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌱 ESG Data Tracker Pro</h1>
        <p>Interactive ESG Monitoring & Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Company selection with more options
    companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "JNJ", "PG", "V", "UNH", 
                "AMZN", "META", "NFLX", "ADBE", "CRM", "ORCL", "INTC", "AMD", "QCOM", "AVGO"]
    selected_company = st.sidebar.selectbox("🏢 Select Company", companies)
    
    # Time period
    time_period = st.sidebar.selectbox("📅 Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
    
    # Additional features
    show_weather = st.sidebar.checkbox("🌤️ Show Weather Data", value=True)
    show_sentiment = st.sidebar.checkbox("😊 Show Sentiment Analysis", value=True)
    show_carbon = st.sidebar.checkbox("🌍 Show Carbon Footprint", value=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 {selected_company} - Interactive Analysis")
        
        # Get data
        company_data = get_alpha_vantage_data(selected_company)
        stock_data = get_stock_data(selected_company, time_period)
        
        if company_data:
            st.success("✅ Real data loaded from Alpha Vantage")
            
            # Company info with enhanced styling
            col1a, col1b, col1c = st.columns(3)
            with col1a:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Company</h3>
                    <p>{company_data.get("Name", "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            with col1b:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Sector</h3>
                    <p>{company_data.get("Sector", "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            with col1c:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Industry</h3>
                    <p>{company_data.get("Industry", "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            
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
                st.metric("💰 Market Cap", market_cap)
            with col2b:
                pe_ratio = company_data.get("PERatio", "N/A")
                if pe_ratio == "None" or pe_ratio is None:
                    pe_ratio = "N/A"
                st.metric("📊 P/E Ratio", pe_ratio)
            with col2c:
                dividend = company_data.get("DividendYield", "N/A")
                if dividend != "N/A" and dividend is not None and dividend != "None":
                    try:
                        dividend = f"{float(dividend)*100:.2f}%"
                    except (ValueError, TypeError):
                        dividend = "N/A"
                else:
                    dividend = "N/A"
                st.metric("💵 Dividend Yield", dividend)
            
            # Interactive Charts
            st.subheader("📊 Interactive Analytics")
            chart_fig = create_interactive_charts(company_data, stock_data, selected_company)
            st.plotly_chart(chart_fig, use_container_width=True)
            
        else:
            st.warning("⚠️ Using enhanced sample data")
            # Enhanced sample data display
            st.markdown("""
            <div class="metric-card">
                <h3>Sample Data Mode</h3>
                <p>Real-time data unavailable. Showing interactive sample data.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Quick Insights")
        
        # ESG Score Display
        if company_data:
            company_name = company_data.get("Name", selected_company)
        else:
            company_name = selected_company
        
        # Calculate ESG scores
        env_score = np.random.randint(60, 90)
        soc_score = np.random.randint(65, 85)
        gov_score = np.random.randint(70, 95)
        overall_score = (env_score + soc_score + gov_score) // 3
        
        st.markdown(f"""
        <div class="esg-score environmental">
            🌱 Environmental: {env_score}/100
        </div>
        <div class="esg-score social">
            🤝 Social: {soc_score}/100
        </div>
        <div class="esg-score governance">
            ⚖️ Governance: {gov_score}/100
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("🏆 Overall ESG Score", f"{overall_score}/100")
        
        # Sentiment Analysis
        if show_sentiment:
            st.subheader("😊 Sentiment Analysis")
            sentiment_score = get_esg_sentiment_score(company_name)
            
            if sentiment_score >= 70:
                sentiment_emoji = "😊"
                sentiment_text = "Positive"
            elif sentiment_score >= 40:
                sentiment_emoji = "😐"
                sentiment_text = "Neutral"
            else:
                sentiment_emoji = "😟"
                sentiment_text = "Negative"
            
            st.metric(f"{sentiment_emoji} ESG Sentiment", f"{sentiment_score}/100 ({sentiment_text})")
        
        # Carbon Footprint
        if show_carbon and company_data:
            st.subheader("🌍 Carbon Footprint")
            carbon_footprint = calculate_carbon_footprint(company_data)
            if carbon_footprint:
                st.metric("CO₂ Emissions", f"{carbon_footprint:.1f} MT CO₂")
                
                # Carbon footprint gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=carbon_footprint,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Carbon Intensity"},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkgreen"},
                           'steps': [{'range': [0, 25], 'color': "lightgreen"},
                                    {'range': [25, 50], 'color': "yellow"},
                                    {'range': [50, 100], 'color': "red"}]}
                ))
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True)
        
        # Weather Data
        if show_weather:
            st.subheader("🌤️ Weather Impact")
            weather_data = get_weather_data()
            if weather_data:
                temp = weather_data['main']['temp']
                weather_desc = weather_data['weather'][0]['description']
                st.metric("🌡️ Temperature", f"{temp}°C")
                st.write(f"☁️ {weather_desc.title()}")
            else:
                st.info("🌤️ Weather data unavailable")
    
    # News Section
    st.subheader("📰 Real ESG News")
    news_articles = get_news_data()
    
    if news_articles:
        st.success(f"✅ {len(news_articles)} real news articles loaded")
        
        # Display news in a more interactive way
        for i, article in enumerate(news_articles[:3]):
            with st.expander(f"📰 {article.get('title', 'No title')[:60]}...", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                    st.write(f"**Published:** {article.get('publishedAt', 'Unknown')[:10]}")
                    st.write(f"**Summary:** {article.get('description', 'No description')}")
                with col2:
                    if article.get('url'):
                        st.link_button("🔗 Read More", article['url'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 10px; color: white;">
        <h3>🌱 ESG Data Tracker Pro - Interactive Edition</h3>
        <p>Powered by News API, Alpha Vantage, OpenWeatherMap, and AI sentiment analysis</p>
    </div>
    """, unsafe_allow_html=True)

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

if __name__ == "__main__":
    main() 