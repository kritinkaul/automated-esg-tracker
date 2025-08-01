#!/usr/bin/env python3
"""
Real Data Collection Script
Collects real ESG data using your API keys
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collection.yahoo_finance_collector import YahooFinanceCollector
from data_collection.news_api_collector import NewsAPICollector
from data_collection.alpha_vantage_collector import AlphaVantageCollector
from data_processing.sentiment_analyzer import SentimentAnalyzer


def main():
    """Collect real data for sample companies"""
    print("🚀 Starting Real Data Collection")
    print("=" * 50)
    
    # Initialize collectors
    yahoo_collector = YahooFinanceCollector()
    news_collector = NewsAPICollector()
    alpha_collector = AlphaVantageCollector()
    sentiment_analyzer = SentimentAnalyzer()
    
    # Sample companies
    companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    total_data = {
        "companies": {},
        "total_esg_scores": 0,
        "total_news": 0,
        "errors": []
    }
    
    for i, ticker in enumerate(companies, 1):
        print(f"\n📊 Processing {ticker} ({i}/{len(companies)})")
        print("-" * 30)
        
        company_data = {
            "ticker": ticker,
            "company_info": None,
            "esg_scores": [],
            "news": [],
            "financial_data": None,
            "errors": []
        }
        
        try:
            # 1. Get company info from Yahoo Finance
            print(f"  🔍 Getting company info...")
            company_info = yahoo_collector.get_company_info(ticker)
            if company_info:
                company_data["company_info"] = company_info
                print(f"  ✅ Company: {company_info['name']}")
            else:
                company_data["errors"].append("Failed to get company info")
                print(f"  ❌ Failed to get company info")
            
            # 2. Get ESG scores
            print(f"  📈 Getting ESG scores...")
            esg_scores = yahoo_collector.get_esg_scores(ticker, days_back=30)
            company_data["esg_scores"] = esg_scores
            total_data["total_esg_scores"] += len(esg_scores)
            print(f"  ✅ ESG scores: {len(esg_scores)} records")
            
            # 3. Get news from Yahoo Finance
            print(f"  📰 Getting news from Yahoo Finance...")
            yahoo_news = yahoo_collector.get_news(ticker, days_back=30)
            company_data["news"].extend(yahoo_news)
            
            # 4. Get news from News API
            if company_info and company_info.get("name"):
                print(f"  📰 Getting news from News API...")
                news_api_news = news_collector.get_esg_news(company_info["name"], days_back=30)
                company_data["news"].extend(news_api_news)
            
            # 5. Analyze sentiment for all news
            if company_data["news"]:
                print(f"  🧠 Analyzing sentiment for {len(company_data['news'])} articles...")
                analyzed_news = sentiment_analyzer.analyze_news_batch(company_data["news"])
                company_data["news"] = analyzed_news
                total_data["total_news"] += len(analyzed_news)
                print(f"  ✅ News articles: {len(analyzed_news)}")
            
            # 6. Get additional data from Alpha Vantage
            print(f"  📊 Getting Alpha Vantage data...")
            alpha_overview = alpha_collector.get_company_overview(ticker)
            if alpha_overview:
                company_data["financial_data"] = alpha_overview
                print(f"  ✅ Alpha Vantage data received")
            
            # 7. Get sentiment from Alpha Vantage
            alpha_sentiment = alpha_collector.get_sentiment_analysis(ticker)
            if alpha_sentiment:
                company_data["alpha_sentiment"] = alpha_sentiment
                print(f"  ✅ Alpha Vantage sentiment: {alpha_sentiment['sentiment_label']}")
            
        except Exception as e:
            error_msg = f"Error processing {ticker}: {e}"
            company_data["errors"].append(error_msg)
            total_data["errors"].append(error_msg)
            print(f"  ❌ {error_msg}")
        
        total_data["companies"][ticker] = company_data
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Data Collection Summary")
    print("=" * 50)
    
    print(f"Companies processed: {len(companies)}")
    print(f"Total ESG scores: {total_data['total_esg_scores']}")
    print(f"Total news articles: {total_data['total_news']}")
    print(f"Errors: {len(total_data['errors'])}")
    
    print("\n📋 Company Details:")
    for ticker, data in total_data["companies"].items():
        print(f"  {ticker}:")
        if data["company_info"]:
            print(f"    Company: {data['company_info']['name']}")
        print(f"    ESG Scores: {len(data['esg_scores'])}")
        print(f"    News Articles: {len(data['news'])}")
        if data["errors"]:
            print(f"    Errors: {len(data['errors'])}")
    
    if total_data["errors"]:
        print("\n❌ Errors encountered:")
        for error in total_data["errors"]:
            print(f"  - {error}")
    
    print("\n🎉 Data collection completed!")
    print("Next steps:")
    print("1. Run the dashboard: streamlit run src/visualization/main.py")
    print("2. Check the collected data in your database")


if __name__ == "__main__":
    main()
