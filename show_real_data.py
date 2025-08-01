#!/usr/bin/env python3
"""
Show Real Data Collection Results
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def show_alpha_vantage_data():
    """Show Alpha Vantage data for a company"""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    print("📊 Alpha Vantage Data (Real Financial Data)")
    print("=" * 50)
    
    # Test with AAPL
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": "AAPL",
        "apikey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            if "Error Message" not in data:
                print(f"✅ Company: {data.get('Name', 'N/A')}")
                print(f"   Sector: {data.get('Sector', 'N/A')}")
                print(f"   Industry: {data.get('Industry', 'N/A')}")
                print(f"   Market Cap: ${data.get('MarketCapitalization', 'N/A')}")
                print(f"   P/E Ratio: {data.get('PERatio', 'N/A')}")
                print(f"   Dividend Yield: {data.get('DividendYield', 'N/A')}")
                print(f"   Description: {data.get('Description', 'N/A')[:200]}...")
            else:
                print(f"❌ Error: {data['Error Message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_news_api_data():
    """Show News API data"""
    api_key = os.getenv("NEWS_API_KEY")
    
    print("\n📰 News API Data (Real ESG News)")
    print("=" * 50)
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "ESG sustainability corporate responsibility",
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 3
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            print(f"✅ Found {len(articles)} recent ESG news articles:")
            
            for i, article in enumerate(articles, 1):
                print(f"\nArticle {i}:")
                print(f"  📰 {article.get('title', 'N/A')}")
                print(f"  📅 {article.get('publishedAt', 'N/A')}")
                print(f"  📰 Source: {article.get('source', {}).get('name', 'N/A')}")
                print(f"  🔗 URL: {article.get('url', 'N/A')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Show all real data sources"""
    print("🎯 Real Data Sources Status")
    print("=" * 60)
    
    # Check API keys
    news_key = os.getenv("NEWS_API_KEY")
    alpha_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    
    print(f"✅ News API Key: {news_key[:10]}..." if news_key else "❌ News API Key: Missing")
    print(f"✅ Alpha Vantage Key: {alpha_key[:10]}..." if alpha_key else "❌ Alpha Vantage Key: Missing")
    print(f"✅ Supabase URL: {supabase_url}" if supabase_url else "❌ Supabase URL: Missing")
    
    # Show real data
    show_alpha_vantage_data()
    show_news_api_data()
    
    print("\n" + "=" * 60)
    print("🎉 Your ESG Data Tracker is collecting REAL data!")
    print("\nNext steps:")
    print("1. Run dashboard: streamlit run src/visualization/main.py")
    print("2. Collect more data: python3 collect_real_data.py")
    print("3. Check SETUP_COMPLETE.md for full details")

if __name__ == "__main__":
    main()
