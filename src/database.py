"""
Database utilities for the ESG Data Tracker.
Handles Supabase connection and SQLAlchemy models.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from supabase import create_client, Client
from src.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()


class Company(Base):
    """Company information table."""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float)
    country = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ESGScores(Base):
    """ESG scores table."""
    __tablename__ = "esg_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    environmental_score = Column(Float)
    social_score = Column(Float)
    governance_score = Column(Float)
    overall_score = Column(Float)
    data_source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class News(Base):
    """ESG-related news table."""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    headline = Column(Text, nullable=False)
    content = Column(Text)
    source = Column(String(100))
    url = Column(String(500))
    sentiment_score = Column(Float)
    sentiment_label = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)


class Metrics(Base):
    """Detailed ESG metrics table."""
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    carbon_emissions = Column(Float)
    renewable_energy_usage = Column(Float)
    board_diversity = Column(Float)
    gender_pay_gap = Column(Float)
    employee_satisfaction = Column(Float)
    data_source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Database manager for handling Supabase and SQLAlchemy operations."""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.engine = None
        self.SessionLocal = None
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize database connections."""
        try:
            # Initialize SQLAlchemy engine (for local development)
            if settings.environment == "development":
                # Use SQLite for local development
                self.engine = create_engine("sqlite:///./esg_data.db")
                Base.metadata.create_all(bind=self.engine)
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                logger.info("SQLAlchemy engine initialized for local development")
            else:
                # Initialize Supabase client for production
                self.supabase = create_client(settings.supabase_url, settings.supabase_key)
                logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database session not initialized")
        return self.SessionLocal()
    
    def insert_company(self, company_data: Dict[str, Any]) -> int:
        """Insert a new company into the database."""
        try:
            if settings.environment == "development":
                # Use SQLAlchemy for local development
                with self.get_session() as session:
                    company = Company(**company_data)
                    session.add(company)
                    session.commit()
                    session.refresh(company)
                    return company.id
            else:
                # Use Supabase for production
                result = self.supabase.table("companies").insert(company_data).execute()
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert company: {e}")
            raise
    
    def insert_esg_scores(self, scores_data: Dict[str, Any]) -> int:
        """Insert ESG scores into the database."""
        try:
            if settings.environment == "development":
                with self.get_session() as session:
                    scores = ESGScores(**scores_data)
                    session.add(scores)
                    session.commit()
                    session.refresh(scores)
                    return scores.id
            else:
                result = self.supabase.table("esg_scores").insert(scores_data).execute()
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert ESG scores: {e}")
            raise
    
    def insert_news(self, news_data: Dict[str, Any]) -> int:
        """Insert news article into the database."""
        try:
            if settings.environment == "development":
                with self.get_session() as session:
                    news = News(**news_data)
                    session.add(news)
                    session.commit()
                    session.refresh(news)
                    return news.id
            else:
                result = self.supabase.table("news").insert(news_data).execute()
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert news: {e}")
            raise
    
    def get_company_by_ticker(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get company information by ticker symbol."""
        try:
            if settings.environment == "development":
                with self.get_session() as session:
                    company = session.query(Company).filter(Company.ticker == ticker).first()
                    return company.__dict__ if company else None
            else:
                result = self.supabase.table("companies").select("*").eq("ticker", ticker).execute()
                return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get company by ticker: {e}")
            return None
    
    def get_esg_scores_history(self, company_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get ESG scores history for a company."""
        try:
            if settings.environment == "development":
                with self.get_session() as session:
                    scores = session.query(ESGScores).filter(
                        ESGScores.company_id == company_id
                    ).order_by(ESGScores.date.desc()).limit(days).all()
                    return [score.__dict__ for score in scores]
            else:
                result = self.supabase.table("esg_scores").select("*").eq(
                    "company_id", company_id
                ).order("date", desc=True).limit(days).execute()
                return result.data
        except Exception as e:
            logger.error(f"Failed to get ESG scores history: {e}")
            return []
    
    def get_latest_news(self, company_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest news for a company."""
        try:
            if settings.environment == "development":
                with self.get_session() as session:
                    news = session.query(News).filter(
                        News.company_id == company_id
                    ).order_by(News.date.desc()).limit(limit).all()
                    return [article.__dict__ for article in news]
            else:
                result = self.supabase.table("news").select("*").eq(
                    "company_id", company_id
                ).order("date", desc=True).limit(limit).execute()
                return result.data
        except Exception as e:
            logger.error(f"Failed to get latest news: {e}")
            return []


# Global database manager instance
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return db_manager 