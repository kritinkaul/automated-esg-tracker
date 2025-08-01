"""
News API Collector
Collects ESG-related news from various news APIs
"""

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class NewsAPICollector:
    """Collects ESG news from NewsAPI.org"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def get_esg_news(self, company_name: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get ESG-related news for a company"""
        if not self.api_key:
            logger.warning("No News API key provided")
            return []
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # ESG-related keywords
            esg_keywords = [
                "ESG", "environmental", "sustainability", "carbon", "renewable",
                "social responsibility", "governance", "diversity", "inclusion",
                "climate change", "green energy", "corporate responsibility"
            ]
            
            all_news = []
            
            for keyword in esg_keywords:
                query = f"{company_name} {keyword}"
                
                params = {
                    "q": query,
                    "from": start_date.strftime("%Y-%m-%d"),
                    "to": end_date.strftime("%Y-%m-%d"),
                    "sortBy": "publishedAt",
                    "apiKey": self.api_key,
                    "language": "en"
                }
                
                response = requests.get(f"{self.base_url}/everything", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    
                    for article in articles:
                        all_news.append({
                            "date": article.get("publishedAt", ""),
                            "headline": article.get("title", ""),
                            "content": article.get("description", ""),
                            "source": article.get("source", {}).get("name", ""),
                            "url": article.get("url", ""),
                            "sentiment_score": 0.0,
                            "sentiment_label": "neutral",
                            "data_source": "news_api",
                            "keyword": keyword
                        })
                else:
                    logger.warning(f"News API request failed: {response.status_code}")
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_news = []
            for article in all_news:
                if article["url"] not in seen_urls:
                    seen_urls.add(article["url"])
                    unique_news.append(article)
            
            return unique_news
            
        except Exception as e:
            logger.error(f"Error getting news for {company_name}: {e}")
            return []
