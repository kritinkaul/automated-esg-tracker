#!/usr/bin/env python3
"""
Setup script for Supabase database
Creates tables and populates with sample ESG data
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import DatabaseManager
from src.config import settings

def test_connection():
    """Test the Supabase connection."""
    print("🔌 Testing Supabase Connection...")
    print(f"📍 Supabase URL: {settings.supabase_url}")
    print(f"🌍 Environment: {settings.environment}")
    
    try:
        db = DatabaseManager()
        if db.supabase:
            print("✅ Supabase connection successful!")
            return db
        else:
            print("❌ Supabase connection failed")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def create_tables_in_supabase(db):
    """Create the required tables in Supabase."""
    print("\n🏗️ Setting up database tables...")
    
    # SQL commands to create tables
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(100),
            industry VARCHAR(100),
            market_cap BIGINT,
            country VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS esg_scores (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            environmental_score FLOAT,
            social_score FLOAT,
            governance_score FLOAT,
            overall_score FLOAT,
            data_source VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            title TEXT NOT NULL,
            content TEXT,
            url TEXT,
            sentiment_score FLOAT,
            source VARCHAR(100),
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            metric_name VARCHAR(100) NOT NULL,
            value FLOAT,
            data_source VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    try:
        for i, sql in enumerate(sql_commands, 1):
            result = db.supabase.rpc('exec_sql', {'sql': sql}).execute()
            print(f"✅ Table {i}/4 created successfully")
        
        print("🎉 All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("📝 Note: Tables might already exist or need to be created manually in Supabase dashboard")
        return False

def insert_sample_data(db):
    """Insert sample ESG data into the database."""
    print("\n📊 Inserting sample data...")
    
    # Sample companies
    companies = [
        {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "market_cap": 3200000000000,
            "country": "USA"
        },
        {
            "ticker": "MSFT",
            "name": "Microsoft Corporation",
            "sector": "Technology",
            "industry": "Software",
            "market_cap": 3100000000000,
            "country": "USA"
        },
        {
            "ticker": "GOOGL",
            "name": "Alphabet Inc.",
            "sector": "Technology",
            "industry": "Internet Services",
            "market_cap": 2000000000000,
            "country": "USA"
        },
        {
            "ticker": "TSLA",
            "name": "Tesla, Inc.",
            "sector": "Consumer Discretionary",
            "industry": "Electric Vehicles",
            "market_cap": 900000000000,
            "country": "USA"
        },
        {
            "ticker": "NVDA",
            "name": "NVIDIA Corporation",
            "sector": "Technology",
            "industry": "Semiconductors",
            "market_cap": 1500000000000,
            "country": "USA"
        }
    ]
    
    try:
        # Insert companies
        for company in companies:
            try:
                result = db.supabase.table("companies").insert(company).execute()
                print(f"✅ Inserted company: {company['ticker']}")
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print(f"ℹ️ Company {company['ticker']} already exists")
                else:
                    print(f"⚠️ Error inserting {company['ticker']}: {e}")
        
        # Get company IDs for ESG scores
        companies_result = db.supabase.table("companies").select("id, ticker").execute()
        company_map = {comp['ticker']: comp['id'] for comp in companies_result.data}
        
        # Sample ESG scores
        esg_scores = [
            {"ticker": "AAPL", "environmental": 75.5, "social": 82.3, "governance": 77.8, "overall": 78.5},
            {"ticker": "MSFT", "environmental": 85.2, "social": 88.1, "governance": 85.0, "overall": 86.1},
            {"ticker": "GOOGL", "environmental": 81.0, "social": 84.5, "governance": 80.2, "overall": 81.9},
            {"ticker": "TSLA", "environmental": 92.0, "social": 88.5, "governance": 93.1, "overall": 91.2},
            {"ticker": "NVDA", "environmental": 73.2, "social": 79.1, "governance": 76.5, "overall": 76.3}
        ]
        
        for score in esg_scores:
            if score['ticker'] in company_map:
                esg_data = {
                    "company_id": company_map[score['ticker']],
                    "environmental_score": score['environmental'],
                    "social_score": score['social'],
                    "governance_score": score['governance'],
                    "overall_score": score['overall'],
                    "data_source": "Sample Data"
                }
                
                try:
                    result = db.supabase.table("esg_scores").insert(esg_data).execute()
                    print(f"✅ Inserted ESG scores for: {score['ticker']}")
                except Exception as e:
                    print(f"⚠️ Error inserting ESG scores for {score['ticker']}: {e}")
        
        # Sample news
        sample_news = [
            {
                "ticker": "AAPL",
                "title": "Apple Announces New Sustainability Initiative",
                "content": "Apple Inc. today announced ambitious new environmental goals...",
                "url": "https://example.com/apple-sustainability",
                "sentiment_score": 0.85,
                "source": "Reuters"
            },
            {
                "ticker": "TSLA",
                "title": "Tesla Leads in Electric Vehicle ESG Performance",
                "content": "Tesla continues to set standards in environmental sustainability...",
                "url": "https://example.com/tesla-esg",
                "sentiment_score": 0.92,
                "source": "Bloomberg"
            }
        ]
        
        for news in sample_news:
            if news['ticker'] in company_map:
                news_data = {
                    "company_id": company_map[news['ticker']],
                    "title": news['title'],
                    "content": news['content'],
                    "url": news['url'],
                    "sentiment_score": news['sentiment_score'],
                    "source": news['source'],
                    "published_at": datetime.utcnow().isoformat()
                }
                
                try:
                    result = db.supabase.table("news").insert(news_data).execute()
                    print(f"✅ Inserted news for: {news['ticker']}")
                except Exception as e:
                    print(f"⚠️ Error inserting news for {news['ticker']}: {e}")
        
        print("🎉 Sample data inserted successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def verify_data(db):
    """Verify that data was inserted correctly."""
    print("\n🔍 Verifying database data...")
    
    try:
        # Check companies
        companies = db.supabase.table("companies").select("*").execute()
        print(f"📊 Companies in database: {len(companies.data)}")
        
        # Check ESG scores
        esg_scores = db.supabase.table("esg_scores").select("*").execute()
        print(f"🌱 ESG scores in database: {len(esg_scores.data)}")
        
        # Check news
        news = db.supabase.table("news").select("*").execute()
        print(f"📰 News articles in database: {len(news.data)}")
        
        # Display sample data
        if companies.data:
            print("\n📋 Sample Companies:")
            for company in companies.data[:3]:
                print(f"   • {company['ticker']}: {company['name']}")
        
        if esg_scores.data:
            print("\n🌟 Sample ESG Scores:")
            for score in esg_scores.data[:3]:
                company_ticker = next((c['ticker'] for c in companies.data if c['id'] == score['company_id']), 'Unknown')
                print(f"   • {company_ticker}: Overall ESG Score {score['overall_score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main setup function."""
    print("🌱 ESG Data Tracker - Supabase Setup")
    print("=" * 50)
    
    # Test connection
    db = test_connection()
    if not db:
        print("❌ Cannot proceed without database connection")
        return
    
    # Note about table creation
    print("\n📝 Note: Due to Supabase security, tables should be created manually.")
    print("👉 Please create tables in your Supabase dashboard using the SQL editor:")
    print("   1. Go to https://zwrzdvplhhktmbpramek.supabase.co")
    print("   2. Navigate to SQL Editor")
    print("   3. Run the table creation SQL commands")
    
    # Try to insert sample data
    print("\n⏩ Attempting to insert sample data...")
    insert_sample_data(db)
    
    # Verify data
    verify_data(db)
    
    print("\n✅ Supabase setup completed!")
    print("🚀 You can now run your dashboard with PostgreSQL backend!")
    print("   streamlit run dashboard_db_integration.py")

if __name__ == "__main__":
    main() 