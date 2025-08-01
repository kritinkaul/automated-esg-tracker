"""
Yahoo Finance Data Collector
Collects real financial and ESG data from Yahoo Finance API
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class YahooFinanceCollector:
    """Collects real data from Yahoo Finance API"""
    
    def __init__(self):
        self.session = None
    
    def get_company_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get basic company information from Yahoo Finance
        
        Args:
            ticker: Company ticker symbol
            
        Returns:
            Dictionary with company information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                "name": info.get("longName", info.get("shortName", ticker)),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap", 0),
                "country": info.get("country", "Unknown"),
                "website": info.get("website", ""),
                "employees": info.get("fullTimeEmployees", 0),
                "description": info.get("longBusinessSummary", "")
            }
        except Exception as e:
            logger.error(f"Error getting company info for {ticker}: {e}")
            return None
    
    def get_esg_scores(self, ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get ESG scores from Yahoo Finance (if available)
        
        Args:
            ticker: Company ticker symbol
            days_back: Number of days of historical data
            
        Returns:
            List of ESG score dictionaries
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Get sustainability data
            sustainability = stock.sustainability
            
            if sustainability is None or sustainability.empty:
                logger.warning(f"No sustainability data available for {ticker}")
                return []
            
            # Convert to our format
            scores = []
            for date, row in sustainability.iterrows():
                scores.append({
                    "date": date.isoformat(),
                    "environmental_score": self._extract_score(row, "environmentalScore"),
                    "social_score": self._extract_score(row, "socialScore"),
                    "governance_score": self._extract_score(row, "governanceScore"),
                    "overall_score": self._extract_score(row, "totalEsg"),
                    "data_source": "yahoo_finance"
                })
            
            return scores
            
        except Exception as e:
            logger.error(f"Error getting ESG scores for {ticker}: {e}")
            return []
    
    def get_financial_metrics(self, ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get financial metrics that might correlate with ESG performance
        
        Args:
            ticker: Company ticker symbol
            days_back: Number of days of historical data
            
        Returns:
            List of financial metrics
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            hist = stock.history(start=start_date, end=end_date)
            
            metrics = []
            for date, row in hist.iterrows():
                metrics.append({
                    "date": date.isoformat(),
                    "stock_price": float(row["Close"]),
                    "volume": int(row["Volume"]),
                    "market_cap": float(row["Close"] * stock.info.get("sharesOutstanding", 0)),
                    "data_source": "yahoo_finance"
                })
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting financial metrics for {ticker}: {e}")
            return []
    
    def get_news(self, ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Get news articles from Yahoo Finance
        
        Args:
            ticker: Company ticker symbol
            days_back: Number of days of historical data
            
        Returns:
            List of news dictionaries
        """
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                return []
            
            # Filter news by date
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            filtered_news = []
            for article in news:
                pub_time = datetime.fromtimestamp(article.get("providerPublishTime", 0))
                
                if pub_time >= cutoff_date:
                    filtered_news.append({
                        "date": pub_time.isoformat(),
                        "headline": article.get("title", ""),
                        "content": article.get("summary", ""),
                        "source": article.get("publisher", ""),
                        "url": article.get("link", ""),
                        "sentiment_score": 0.0,  # Will be calculated separately
                        "sentiment_label": "neutral",
                        "data_source": "yahoo_finance"
                    })
            
            return filtered_news
            
        except Exception as e:
            logger.error(f"Error getting news for {ticker}: {e}")
            return []
    
    def _extract_score(self, row: pd.Series, column: str) -> float:
        """Extract and normalize score from Yahoo Finance data"""
        try:
            value = row.get(column, 0)
            if pd.isna(value) or value is None:
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def get_all_data(self, ticker: str, days_back: int = 30) -> Dict[str, Any]:
        """
        Get all available data for a company
        
        Args:
            ticker: Company ticker symbol
            days_back: Number of days of historical data
            
        Returns:
            Dictionary with all collected data
        """
        return {
            "company_info": self.get_company_info(ticker),
            "esg_scores": self.get_esg_scores(ticker, days_back),
            "financial_metrics": self.get_financial_metrics(ticker, days_back),
            "news": self.get_news(ticker, days_back)
        }
