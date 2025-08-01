"""
Main data collection script for ESG Data Tracker.
Fetches ESG data from various sources and stores in database.
"""

import logging
import time
import requests
import yfinance as yf
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import settings
from utils.database import get_db_manager
from utils.mock_data import SAMPLE_COMPANIES, generate_esg_scores, generate_news

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ESGDataCollector:
    """Main class for collecting ESG data from various sources."""
    
    def __init__(self):
        self.db_manager = get_db_manager()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ESG-Data-Tracker/1.0 (Educational Project)'
        })
    
    def collect_company_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Collect basic company information using Yahoo Finance.
        
        Args:
            ticker: Company ticker symbol
            
        Returns:
            Dictionary with company information or None if failed
        """
        try:
            logger.info(f"Collecting company info for {ticker}")
            
            # Use yfinance to get company info
            stock = yf.Ticker(ticker)
            info = stock.info
            
            company_data = {
                "ticker": ticker,
                "name": info.get('longName', info.get('shortName', ticker)),
                "sector": info.get('sector', 'Unknown'),
                "industry": info.get('industry', 'Unknown'),
                "market_cap": info.get('marketCap', 0),
                "country": info.get('country', 'Unknown')
            }
            
            logger.info(f"Successfully collected info for {ticker}: {company_data['name']}")
            return company_data
            
        except Exception as e:
            logger.error(f"Failed to collect company info for {ticker}: {e}")
            return None
    
    def collect_esg_scores(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Collect ESG scores for a company.
        Currently uses mock data, but can be extended with real APIs.
        
        Args:
            ticker: Company ticker symbol
            
        Returns:
            Dictionary with ESG scores or None if failed
        """
        try:
            logger.info(f"Collecting ESG scores for {ticker}")
            
            # For now, use mock data
            # In production, this would call real ESG APIs like:
            # - ESG Book API
            # - Sustainalytics API
            # - MSCI ESG API
            
            # Generate mock ESG scores for today
            mock_scores = generate_esg_scores(ticker, days_back=1)
            if mock_scores:
                scores = mock_scores[0]
                scores['data_source'] = 'mock_data'
                return scores
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to collect ESG scores for {ticker}: {e}")
            return None
    
    def collect_news(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        """
        Collect ESG-related news for a company.
        
        Args:
            ticker: Company ticker symbol
            company_name: Company name for news search
            
        Returns:
            List of news articles
        """
        try:
            logger.info(f"Collecting news for {ticker}")
            
            # For now, use mock data
            # In production, this would call news APIs like:
            # - NewsAPI
            # - Alpha Vantage News
            # - Yahoo Finance News
            
            mock_news = generate_news(ticker, days_back=5)
            return mock_news
            
        except Exception as e:
            logger.error(f"Failed to collect news for {ticker}: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of news text using Hugging Face transformers.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment score and label
        """
        try:
            # For now, return mock sentiment
            # In production, this would use:
            # from transformers import pipeline
            # classifier = pipeline("sentiment-analysis")
            # result = classifier(text)
            
            import random
            sentiment_score = random.uniform(-1, 1)
            
            if sentiment_score > 0.3:
                label = "positive"
            elif sentiment_score < -0.3:
                label = "negative"
            else:
                label = "neutral"
            
            return {
                "sentiment_score": round(sentiment_score, 3),
                "sentiment_label": label
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {"sentiment_score": 0.0, "sentiment_label": "neutral"}
    
    def process_company(self, ticker: str) -> bool:
        """
        Process a single company: collect all data and store in database.
        
        Args:
            ticker: Company ticker symbol
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Processing company: {ticker}")
            
            # Check if company already exists
            existing_company = self.db_manager.get_company_by_ticker(ticker)
            
            if existing_company:
                company_id = existing_company['id']
                logger.info(f"Company {ticker} already exists with ID {company_id}")
            else:
                # Collect company information
                company_data = self.collect_company_info(ticker)
                if not company_data:
                    logger.error(f"Failed to collect company info for {ticker}")
                    return False
                
                # Insert company into database
                company_id = self.db_manager.insert_company(company_data)
                logger.info(f"Inserted company {ticker} with ID {company_id}")
            
            # Collect ESG scores
            esg_data = self.collect_esg_scores(ticker)
            if esg_data:
                esg_data['company_id'] = company_id
                self.db_manager.insert_esg_scores(esg_data)
                logger.info(f"Inserted ESG scores for {ticker}")
            
            # Collect and process news
            company_name = existing_company['name'] if existing_company else ticker
            news_articles = self.collect_news(ticker, company_name)
            
            for article in news_articles:
                # Analyze sentiment
                sentiment = self.analyze_sentiment(article['headline'])
                article['sentiment_score'] = sentiment['sentiment_score']
                article['sentiment_label'] = sentiment['sentiment_label']
                article['company_id'] = company_id
                
                # Insert news article
                self.db_manager.insert_news(article)
            
            logger.info(f"Inserted {len(news_articles)} news articles for {ticker}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process company {ticker}: {e}")
            return False
    
    def collect_all_data(self) -> Dict[str, Any]:
        """
        Collect ESG data for all tracked companies.
        
        Returns:
            Dictionary with collection results
        """
        logger.info("Starting ESG data collection for all companies")
        
        results = {
            "start_time": datetime.now(),
            "companies_processed": 0,
            "companies_successful": 0,
            "companies_failed": 0,
            "errors": []
        }
        
        # Process each company
        for company in SAMPLE_COMPANIES:
            ticker = company['ticker']
            results["companies_processed"] += 1
            
            try:
                success = self.process_company(ticker)
                if success:
                    results["companies_successful"] += 1
                else:
                    results["companies_failed"] += 1
                    results["errors"].append(f"Failed to process {ticker}")
                
                # Add delay between requests to be respectful to APIs
                time.sleep(1)
                
            except Exception as e:
                results["companies_failed"] += 1
                results["errors"].append(f"Error processing {ticker}: {str(e)}")
                logger.error(f"Error processing {ticker}: {e}")
        
        results["end_time"] = datetime.now()
        results["duration"] = results["end_time"] - results["start_time"]
        
        logger.info(f"Data collection completed: {results['companies_successful']} successful, "
                   f"{results['companies_failed']} failed")
        
        return results


def main():
    """Main function to run the data collection."""
    try:
        collector = ESGDataCollector()
        results = collector.collect_all_data()
        
        # Log results
        logger.info("=== Data Collection Results ===")
        logger.info(f"Companies processed: {results['companies_processed']}")
        logger.info(f"Successful: {results['companies_successful']}")
        logger.info(f"Failed: {results['companies_failed']}")
        logger.info(f"Duration: {results['duration']}")
        
        if results['errors']:
            logger.error("Errors encountered:")
            for error in results['errors']:
                logger.error(f"  - {error}")
        
        return results
        
    except Exception as e:
        logger.error(f"Fatal error in data collection: {e}")
        raise


if __name__ == "__main__":
    main() 