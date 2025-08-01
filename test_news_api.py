#!/usr/bin/env python3
"""
Test News API specifically
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_news_api():
    """Test News API with your key"""
    api_key = os.getenv("NEWS_API_KEY")
    print(f"Testing News API with key: {api_key[:10]}...")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Apple ESG sustainability",
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            print(f"Found {len(articles)} articles")
            
            for i, article in enumerate(articles[:3], 1):
                print(f"\nArticle {i}:")
                print(f"  Title: {article.get('title', 'N/A')}")
                print(f"  Source: {article.get('source', {}).get('name', 'N/A')}")
                print(f"  Published: {article.get('publishedAt', 'N/A')}")
                print(f"  URL: {article.get('url', 'N/A')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing News API: {e}")

if __name__ == "__main__":
    test_news_api()
