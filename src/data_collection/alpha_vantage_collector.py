"""
Alpha Vantage Data Collector
Collects additional financial and ESG data from Alpha Vantage API
"""

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AlphaVantageCollector:
    """Collects data from Alpha Vantage API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_company_overview(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get detailed company overview"""
        if not self.api_key:
            logger.warning("No Alpha Vantage API key provided")
            return None
        
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": ticker,
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if "Error Message" in data:
                    logger.warning(f"Alpha Vantage error for {ticker}: {data['Error Message']}")
                    return None
                
                return {
                    "ticker": ticker,
                    "name": data.get("Name", ""),
                    "sector": data.get("Sector", ""),
                    "industry": data.get("Industry", ""),
                    "market_cap": data.get("MarketCapitalization", ""),
                    "pe_ratio": data.get("PERatio", ""),
                    "dividend_yield": data.get("DividendYield", ""),
                    "description": data.get("Description", ""),
                    "data_source": "alpha_vantage"
                }
            else:
                logger.warning(f"Alpha Vantage request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting company overview for {ticker}: {e}")
            return None
    
    def get_earnings_calendar(self, ticker: str) -> List[Dict[str, Any]]:
        """Get earnings calendar data"""
        if not self.api_key:
            return []
        
        try:
            params = {
                "function": "EARNINGS_CALENDAR",
                "symbol": ticker,
                "horizon": "3month",
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                # This returns CSV data
                lines = response.text.strip().split('\n')
                if len(lines) < 2:
                    return []
                
                headers = lines[0].split(',')
                earnings = []
                
                for line in lines[1:]:
                    values = line.split(',')
                    if len(values) == len(headers):
                        earnings.append(dict(zip(headers, values)))
                
                return earnings
            else:
                logger.warning(f"Alpha Vantage earnings request failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting earnings for {ticker}: {e}")
            return []
    
    def get_sentiment_analysis(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get news sentiment analysis"""
        if not self.api_key:
            return None
        
        try:
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": ticker,
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if "feed" in data and data["feed"]:
                    # Get the most recent sentiment data
                    latest_news = data["feed"][0]
                    
                    return {
                        "ticker": ticker,
                        "sentiment_score": latest_news.get("overall_sentiment_score", 0),
                        "sentiment_label": latest_news.get("overall_sentiment_label", "neutral"),
                        "news_count": len(data["feed"]),
                        "data_source": "alpha_vantage"
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting sentiment for {ticker}: {e}")
            return None
