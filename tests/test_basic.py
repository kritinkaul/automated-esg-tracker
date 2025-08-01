"""
Basic tests for ESG Data Tracker.
Tests core functionality and data structures.
"""

import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.mock_data import SAMPLE_COMPANIES, generate_esg_scores, generate_news
from utils.config import settings


class TestMockData:
    """Test mock data generation functionality."""
    
    def test_sample_companies_structure(self):
        """Test that sample companies have correct structure."""
        assert len(SAMPLE_COMPANIES) > 0
        
        for company in SAMPLE_COMPANIES:
            assert 'ticker' in company
            assert 'name' in company
            assert 'sector' in company
            assert 'industry' in company
            assert 'market_cap' in company
            assert 'country' in company
    
    def test_generate_esg_scores(self):
        """Test ESG score generation."""
        ticker = "AAPL"
        scores = generate_esg_scores(ticker, days_back=5)
        
        assert len(scores) == 5
        
        for score in scores:
            assert 'date' in score
            assert 'environmental_score' in score
            assert 'social_score' in score
            assert 'governance_score' in score
            assert 'overall_score' in score
            assert 'data_source' in score
            
            # Check score ranges
            assert 0 <= score['environmental_score'] <= 100
            assert 0 <= score['social_score'] <= 100
            assert 0 <= score['governance_score'] <= 100
            assert 0 <= score['overall_score'] <= 100
    
    def test_generate_news(self):
        """Test news generation."""
        ticker = "TSLA"
        news = generate_news(ticker, days_back=3)
        
        assert len(news) == 3
        
        for article in news:
            assert 'date' in article
            assert 'headline' in article
            assert 'content' in article
            assert 'source' in article
            assert 'url' in article
            assert 'sentiment_score' in article
            assert 'sentiment_label' in article
            
            # Check sentiment score range
            assert -1 <= article['sentiment_score'] <= 1
            
            # Check sentiment label
            assert article['sentiment_label'] in ['positive', 'negative', 'neutral']


class TestConfiguration:
    """Test configuration management."""
    
    def test_settings_loaded(self):
        """Test that settings are loaded correctly."""
        assert hasattr(settings, 'environment')
        assert hasattr(settings, 'log_level')
        assert hasattr(settings, 'debug')
    
    def test_environment_modes(self):
        """Test environment mode functions."""
        from utils.config import is_development, is_production
        
        # These should work regardless of current environment
        assert isinstance(is_development(), bool)
        assert isinstance(is_production(), bool)


class TestDataStructures:
    """Test data structure integrity."""
    
    def test_company_tickers_unique(self):
        """Test that all company tickers are unique."""
        tickers = [company['ticker'] for company in SAMPLE_COMPANIES]
        assert len(tickers) == len(set(tickers))
    
    def test_company_names_not_empty(self):
        """Test that company names are not empty."""
        for company in SAMPLE_COMPANIES:
            assert company['name'].strip() != ""
            assert company['ticker'].strip() != ""


if __name__ == "__main__":
    pytest.main([__file__]) 