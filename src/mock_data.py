"""
Mock data generator for ESG Data Tracker.
Provides realistic ESG data for development and testing purposes.
"""

import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from database import get_db_manager


# Sample companies with realistic ESG profiles
SAMPLE_COMPANIES = [
    {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": 3000000000000,  # 3 trillion
        "country": "USA"
    },
    {
        "ticker": "TSLA",
        "name": "Tesla Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Automobiles",
        "market_cap": 800000000000,  # 800 billion
        "country": "USA"
    },
    {
        "ticker": "JPM",
        "name": "JPMorgan Chase & Co.",
        "sector": "Financial Services",
        "industry": "Banks",
        "market_cap": 500000000000,  # 500 billion
        "country": "USA"
    },
    {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software",
        "market_cap": 2800000000000,  # 2.8 trillion
        "country": "USA"
    },
    {
        "ticker": "GOOGL",
        "name": "Alphabet Inc.",
        "sector": "Technology",
        "industry": "Internet Content & Information",
        "market_cap": 1800000000000,  # 1.8 trillion
        "country": "USA"
    },
    {
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "market_cap": 1200000000000,  # 1.2 trillion
        "country": "USA"
    },
    {
        "ticker": "UNH",
        "name": "UnitedHealth Group Inc.",
        "sector": "Healthcare",
        "industry": "Healthcare Plans",
        "market_cap": 450000000000,  # 450 billion
        "country": "USA"
    },
    {
        "ticker": "JNJ",
        "name": "Johnson & Johnson",
        "sector": "Healthcare",
        "industry": "Drug Manufacturers",
        "market_cap": 400000000000,  # 400 billion
        "country": "USA"
    },
    {
        "ticker": "PG",
        "name": "Procter & Gamble Co.",
        "sector": "Consumer Defensive",
        "industry": "Household & Personal Products",
        "market_cap": 350000000000,  # 350 billion
        "country": "USA"
    },
    {
        "ticker": "V",
        "name": "Visa Inc.",
        "sector": "Financial Services",
        "industry": "Credit Services",
        "market_cap": 500000000000,  # 500 billion
        "country": "USA"
    }
]


def generate_esg_scores(company_ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Generate realistic ESG scores for a company over time.
    
    Args:
        company_ticker: Company ticker symbol
        days_back: Number of days of historical data to generate
    
    Returns:
        List of ESG score dictionaries
    """
    # Base ESG scores by company (realistic values)
    base_scores = {
        "AAPL": {"env": 75, "social": 80, "gov": 85},  # Strong ESG performer
        "TSLA": {"env": 90, "social": 60, "gov": 70},  # Strong environmental, weaker social
        "JPM": {"env": 65, "social": 70, "gov": 75},   # Financial services profile
        "MSFT": {"env": 80, "social": 85, "gov": 90},  # Very strong ESG
        "GOOGL": {"env": 75, "social": 80, "gov": 85}, # Strong ESG
        "NVDA": {"env": 70, "social": 75, "gov": 80},  # Good ESG
        "UNH": {"env": 60, "social": 65, "gov": 70},   # Healthcare profile
        "JNJ": {"env": 70, "social": 75, "gov": 80},   # Healthcare with good ESG
        "PG": {"env": 75, "social": 80, "gov": 85},    # Consumer goods with strong ESG
        "V": {"env": 65, "social": 70, "gov": 75}      # Financial services
    }
    
    base = base_scores.get(company_ticker, {"env": 70, "social": 70, "gov": 70})
    
    scores = []
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        
        # Add realistic variation (±5 points)
        env_score = max(0, min(100, base["env"] + random.uniform(-5, 5)))
        social_score = max(0, min(100, base["social"] + random.uniform(-5, 5)))
        gov_score = max(0, min(100, base["gov"] + random.uniform(-5, 5)))
        
        # Calculate overall score (weighted average)
        overall_score = (env_score * 0.4 + social_score * 0.3 + gov_score * 0.3)
        
        scores.append({
            "date": date.isoformat(),
            "environmental_score": round(env_score, 2),
            "social_score": round(social_score, 2),
            "governance_score": round(gov_score, 2),
            "overall_score": round(overall_score, 2),
            "data_source": "mock_data"
        })
    
    return scores


def generate_metrics(company_ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Generate detailed ESG metrics for a company.
    
    Args:
        company_ticker: Company ticker symbol
        days_back: Number of days of historical data to generate
    
    Returns:
        List of metrics dictionaries
    """
    # Base metrics by company
    base_metrics = {
        "AAPL": {
            "carbon_emissions": 15.0,  # Million tonnes CO2
            "renewable_energy": 85.0,  # Percentage
            "board_diversity": 45.0,   # Percentage women
            "gender_pay_gap": 2.0,     # Percentage
            "employee_satisfaction": 4.2  # 1-5 scale
        },
        "TSLA": {
            "carbon_emissions": 5.0,
            "renewable_energy": 95.0,
            "board_diversity": 30.0,
            "gender_pay_gap": 8.0,
            "employee_satisfaction": 3.8
        },
        "JPM": {
            "carbon_emissions": 25.0,
            "renewable_energy": 60.0,
            "board_diversity": 40.0,
            "gender_pay_gap": 5.0,
            "employee_satisfaction": 3.9
        }
    }
    
    base = base_metrics.get(company_ticker, {
        "carbon_emissions": 20.0,
        "renewable_energy": 70.0,
        "board_diversity": 35.0,
        "gender_pay_gap": 5.0,
        "employee_satisfaction": 4.0
    })
    
    metrics = []
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        
        # Add realistic variation
        carbon = max(0, base["carbon_emissions"] + random.uniform(-2, 2))
        renewable = max(0, min(100, base["renewable_energy"] + random.uniform(-5, 5)))
        diversity = max(0, min(100, base["board_diversity"] + random.uniform(-3, 3)))
        pay_gap = max(0, base["gender_pay_gap"] + random.uniform(-1, 1))
        satisfaction = max(1, min(5, base["employee_satisfaction"] + random.uniform(-0.2, 0.2)))
        
        metrics.append({
            "date": date,
            "carbon_emissions": round(carbon, 2),
            "renewable_energy_usage": round(renewable, 2),
            "board_diversity": round(diversity, 2),
            "gender_pay_gap": round(pay_gap, 2),
            "employee_satisfaction": round(satisfaction, 2),
            "data_source": "mock_data"
        })
    
    return metrics


def generate_news(company_ticker: str, days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Generate mock ESG-related news for a company.
    
    Args:
        company_ticker: Company ticker symbol
        days_back: Number of days of historical data to generate
    
    Returns:
        List of news dictionaries
    """
    # Sample ESG news templates
    news_templates = [
        {
            "headline": f"{company_ticker} Announces New Renewable Energy Initiative",
            "sentiment": 0.8,
            "sentiment_label": "positive"
        },
        {
            "headline": f"{company_ticker} Reports Progress on Carbon Reduction Goals",
            "sentiment": 0.7,
            "sentiment_label": "positive"
        },
        {
            "headline": f"{company_ticker} Faces Criticism Over Board Diversity",
            "sentiment": -0.3,
            "sentiment_label": "negative"
        },
        {
            "headline": f"{company_ticker} Launches Employee Sustainability Program",
            "sentiment": 0.6,
            "sentiment_label": "positive"
        },
        {
            "headline": f"{company_ticker} Releases Annual ESG Report",
            "sentiment": 0.4,
            "sentiment_label": "neutral"
        },
        {
            "headline": f"{company_ticker} Invests in Green Technology Startups",
            "sentiment": 0.9,
            "sentiment_label": "positive"
        },
        {
            "headline": f"{company_ticker} Under Investigation for Environmental Violations",
            "sentiment": -0.7,
            "sentiment_label": "negative"
        }
    ]
    
    news = []
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        
        # Randomly select a news template
        template = random.choice(news_templates)
        
        # Add some variation to sentiment
        sentiment = max(-1, min(1, template["sentiment"] + random.uniform(-0.2, 0.2)))
        
        news.append({
            "date": date.isoformat(),
            "headline": template["headline"],
            "content": f"This is a mock news article about {company_ticker}'s ESG initiatives.",
            "source": "Mock News Agency",
            "url": f"https://mocknews.com/{company_ticker.lower()}-esg-{i}",
            "sentiment_score": round(sentiment, 3),
            "sentiment_label": template["sentiment_label"]
        })
    
    return news


def populate_mock_data():
    """
    Populate the database with mock ESG data for all sample companies.
    """
    db_manager = get_db_manager()
    
    print("Populating database with mock ESG data...")
    
    for company_data in SAMPLE_COMPANIES:
        try:
            # Insert company
            company_id = db_manager.insert_company(company_data)
            print(f"Inserted company: {company_data['ticker']} (ID: {company_id})")
            
            # Generate and insert ESG scores
            esg_scores = generate_esg_scores(company_data['ticker'])
            for score in esg_scores:
                score['company_id'] = company_id
                db_manager.insert_esg_scores(score)
            
            # Generate and insert metrics
            metrics = generate_metrics(company_data['ticker'])
            for metric in metrics:
                metric['company_id'] = company_id
                # Note: We'll need to add this method to DatabaseManager
                # db_manager.insert_metrics(metric)
            
            # Generate and insert news
            news = generate_news(company_data['ticker'])
            for article in news:
                article['company_id'] = company_id
                db_manager.insert_news(article)
            
            print(f"Generated data for {company_data['ticker']}: {len(esg_scores)} scores, {len(news)} news articles")
            
        except Exception as e:
            print(f"Error populating data for {company_data['ticker']}: {e}")
    
    print("Mock data population completed!")


if __name__ == "__main__":
    populate_mock_data() 