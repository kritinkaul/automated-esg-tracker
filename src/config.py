"""
Configuration management for the ESG Data Tracker.
Handles environment variables, API keys, and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    supabase_url: str = Field("mock_url", env="SUPABASE_URL")
    supabase_key: str = Field("mock_key", env="SUPABASE_KEY")
    
    # API Keys
    yahoo_finance_api_key: Optional[str] = Field(None, env="YAHOO_FINANCE_API_KEY")
    alpha_vantage_api_key: Optional[str] = Field(None, env="ALPHA_VANTAGE_API_KEY")
    news_api_key: Optional[str] = Field(None, env="NEWS_API_KEY")
    esg_book_api_key: Optional[str] = Field(None, env="ESG_BOOK_API_KEY")
    huggingface_api_key: Optional[str] = Field(None, env="HUGGINGFACE_API_KEY")
    
    # Application Settings
    environment: str = Field("development", env="ENVIRONMENT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    debug: bool = Field(True, env="DEBUG")
    
    # Data Collection Settings
    data_collection_interval_hours: int = Field(24, env="DATA_COLLECTION_INTERVAL_HOURS")
    max_retries: int = Field(3, env="MAX_RETRIES")
    request_timeout: int = Field(30, env="REQUEST_TIMEOUT")
    
    # Dashboard Settings
    streamlit_server_port: int = Field(8501, env="STREAMLIT_SERVER_PORT")
    streamlit_server_address: str = Field("localhost", env="STREAMLIT_SERVER_ADDRESS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def is_development() -> bool:
    """Check if running in development mode."""
    return settings.environment == "development"


def is_production() -> bool:
    """Check if running in production mode."""
    return settings.environment == "production" 