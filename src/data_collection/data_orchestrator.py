"""
Data Collection Orchestrator
Coordinates data collection from multiple sources
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection.yahoo_finance_collector import YahooFinanceCollector
from data_collection.news_api_collector import NewsAPICollector
from data_collection.alpha_vantage_collector import AlphaVantageCollector
from data_processing.sentiment_analyzer import SentimentAnalyzer
from ..database import get_db_manager

logger = logging.getLogger(__name__)


class DataOrchestrator:
    """Orchestrates data collection from multiple sources"""
    
    def __init__(self):
        self.yahoo_collector = YahooFinanceCollector()
        self.news_collector = NewsAPICollector()
        self.alpha_collector = AlphaVantageCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.db_manager = get_db_manager()
    
    def collect_company_data(self, ticker: str, days_back: int = 30) -> Dict[str, Any]:
        """Collect all available data for a company"""
        logger.info(f"Starting data collection for {ticker}")
        
        collected_data = {
            "ticker": ticker,
            "collection_date": datetime.now().isoformat(),
            "company_info": None,
            "esg_scores": [],
            "news": [],
            "financial_metrics": [],
            "errors": []
        }
        
        try:
            # 1. Get company information from Yahoo Finance
            logger.info(f"Collecting company info for {ticker}")
            company_info = self.yahoo_collector.get_company_info(ticker)
            if company_info:
                collected_data["company_info"] = company_info
            else:
                collected_data["errors"].append("Failed to get company info from Yahoo Finance")
            
            # 2. Get ESG scores from Yahoo Finance
            logger.info(f"Collecting ESG scores for {ticker}")
            esg_scores = self.yahoo_collector.get_esg_scores(ticker, days_back)
            collected_data["esg_scores"] = esg_scores
            
            # 3. Get news from multiple sources
            logger.info(f"Collecting news for {ticker}")
            news_data = []
            
            # Yahoo Finance news
            yahoo_news = self.yahoo_collector.get_news(ticker, days_back)
            news_data.extend(yahoo_news)
            
            # News API (if company name is available)
            if company_info and company_info.get("name"):
                news_api_news = self.news_collector.get_esg_news(company_info["name"], days_back)
                news_data.extend(news_api_news)
            
            # 4. Analyze sentiment for all news
            if news_data:
                logger.info(f"Analyzing sentiment for {len(news_data)} news articles")
                analyzed_news = self.sentiment_analyzer.analyze_news_batch(news_data)
                collected_data["news"] = analyzed_news
            
            # 5. Get additional financial data from Alpha Vantage
            logger.info(f"Collecting additional financial data for {ticker}")
            alpha_overview = self.alpha_collector.get_company_overview(ticker)
            if alpha_overview:
                # Merge with existing company info
                if collected_data["company_info"]:
                    collected_data["company_info"].update(alpha_overview)
                else:
                    collected_data["company_info"] = alpha_overview
            
            # 6. Get sentiment analysis from Alpha Vantage
            alpha_sentiment = self.alpha_collector.get_sentiment_analysis(ticker)
            if alpha_sentiment:
                collected_data["alpha_sentiment"] = alpha_sentiment
            
            logger.info(f"Data collection completed for {ticker}")
            
        except Exception as e:
            error_msg = f"Error collecting data for {ticker}: {e}"
            logger.error(error_msg)
            collected_data["errors"].append(error_msg)
        
        return collected_data
    
    def save_to_database(self, collected_data: Dict[str, Any]) -> bool:
        """Save collected data to database"""
        try:
            ticker = collected_data["ticker"]
            
            # Save company info
            if collected_data["company_info"]:
                company_id = self.db_manager.insert_company(collected_data["company_info"])
                logger.info(f"Saved company info for {ticker} (ID: {company_id})")
            else:
                logger.warning(f"No company info to save for {ticker}")
                return False
            
            # Save ESG scores
            if collected_data["esg_scores"]:
                for score in collected_data["esg_scores"]:
                    score["company_id"] = company_id
                    self.db_manager.insert_esg_scores(score)
                logger.info(f"Saved {len(collected_data['esg_scores'])} ESG scores for {ticker}")
            
            # Save news
            if collected_data["news"]:
                for article in collected_data["news"]:
                    article["company_id"] = company_id
                    self.db_manager.insert_news(article)
                logger.info(f"Saved {len(collected_data['news'])} news articles for {ticker}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving data to database: {e}")
            return False
    
    def collect_all_companies(self, tickers: List[str], days_back: int = 30) -> Dict[str, Any]:
        """Collect data for all specified companies"""
        results = {
            "total_companies": len(tickers),
            "successful": 0,
            "failed": 0,
            "errors": [],
            "companies": {}
        }
        
        for ticker in tickers:
            try:
                logger.info(f"Processing {ticker} ({results['successful'] + results['failed'] + 1}/{len(tickers)})")
                
                # Collect data
                collected_data = self.collect_company_data(ticker, days_back)
                
                # Save to database
                if self.save_to_database(collected_data):
                    results["successful"] += 1
                    results["companies"][ticker] = "success"
                else:
                    results["failed"] += 1
                    results["companies"][ticker] = "failed"
                    results["errors"].append(f"Failed to save data for {ticker}")
                
            except Exception as e:
                results["failed"] += 1
                results["companies"][ticker] = "error"
                error_msg = f"Error processing {ticker}: {e}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"Data collection completed: {results['successful']} successful, {results['failed']} failed")
        return results


def main():
    """Main function for data collection"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Sample companies to collect data for
    sample_tickers = [
        "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "JNJ", "PG", "V", "UNH"
    ]
    
    # Initialize orchestrator
    orchestrator = DataOrchestrator()
    
    # Collect data for all companies
    results = orchestrator.collect_all_companies(sample_tickers, days_back=30)
    
    # Print results
    print(f"\nData Collection Results:")
    print(f"Total companies: {results['total_companies']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    
    if results["errors"]:
        print(f"\nErrors:")
        for error in results["errors"]:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
