#!/usr/bin/env python3
"""
Test script for real data collection
Quick test to verify all data sources are working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_collection.yahoo_finance_collector import YahooFinanceCollector
from src.data_collection.news_api_collector import NewsAPICollector
from src.data_collection.alpha_vantage_collector import AlphaVantageCollector
from src.data_processing.sentiment_analyzer import SentimentAnalyzer


def test_yahoo_finance():
    """Test Yahoo Finance data collection"""
    print("Testing Yahoo Finance...")
    
    collector = YahooFinanceCollector()
    
    # Test company info
    company_info = collector.get_company_info("AAPL")
    if company_info:
        print(f"✅ Company info: {company_info['name']}")
    else:
        print("❌ Failed to get company info")
    
    # Test ESG scores
    esg_scores = collector.get_esg_scores("AAPL", days_back=7)
    print(f"✅ ESG scores: {len(esg_scores)} records")
    
    # Test news
    news = collector.get_news("AAPL", days_back=7)
    print(f"✅ News articles: {len(news)} records")
    
    return True


def test_news_api():
    """Test News API data collection"""
    print("\nTesting News API...")
    
    collector = NewsAPICollector()
    
    # Test news collection
    news = collector.get_esg_news("Apple Inc", days_back=7)
    print(f"✅ ESG news: {len(news)} articles")
    
    return True


def test_alpha_vantage():
    """Test Alpha Vantage data collection"""
    print("\nTesting Alpha Vantage...")
    
    collector = AlphaVantageCollector()
    
    # Test company overview
    overview = collector.get_company_overview("AAPL")
    if overview:
        print(f"✅ Company overview: {overview['name']}")
    else:
        print("❌ Failed to get company overview")
    
    # Test sentiment
    sentiment = collector.get_sentiment_analysis("AAPL")
    if sentiment:
        print(f"✅ Sentiment analysis: {sentiment['sentiment_label']}")
    else:
        print("❌ Failed to get sentiment analysis")
    
    return True


def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\nTesting Sentiment Analysis...")
    
    analyzer = SentimentAnalyzer()
    
    # Test with sample text
    sample_text = "Apple announces new renewable energy initiative to reduce carbon footprint"
    sentiment = analyzer.analyze_esg_sentiment(sample_text)
    
    print(f"✅ Sentiment analysis: {sentiment['sentiment_label']} ({sentiment['sentiment_score']:.2f})")
    
    return True


def main():
    """Run all tests"""
    print("🧪 Testing Real Data Collection")
    print("=" * 50)
    
    tests = [
        test_yahoo_finance,
        test_news_api,
        test_alpha_vantage,
        test_sentiment_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Your real data setup is working.")
    else:
        print("⚠️  Some tests failed. Check your API keys and configuration.")


if __name__ == "__main__":
    main()
