"""
Example usage of PostgreSQL database in ESG Data Tracker
Shows how to insert and retrieve data using the DatabaseManager
"""

from src.database import DatabaseManager
from datetime import datetime

def example_database_usage():
    """Demonstrate how to use the PostgreSQL database."""
    
    # Initialize database manager
    db = DatabaseManager()
    
    # 1. INSERT COMPANY DATA
    company_data = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": 3200000000000,  # $3.2T
        "country": "USA"
    }
    
    try:
        company_id = db.insert_company(company_data)
        print(f"✅ Inserted company with ID: {company_id}")
    except Exception as e:
        print(f"ℹ️ Company might already exist: {e}")
        # Get existing company ID
        try:
            company_result = db.supabase.table("companies").select("id").eq("ticker", "AAPL").execute()
            if company_result.data:
                company_id = company_result.data[0]['id']
                print(f"📋 Using existing company ID: {company_id}")
            else:
                print("❌ Could not find or create company")
                return
        except Exception as e2:
            print(f"❌ Error getting company: {e2}")
            return
    
    # 2. INSERT ESG SCORES
    esg_data = {
        "company_id": company_id,
        "environmental_score": 75.5,
        "social_score": 82.3,
        "governance_score": 77.8,
        "overall_score": 78.5,
        "data_source": "MSCI ESG"
    }
    
    try:
        score_id = db.insert_esg_scores(esg_data)
        print(f"✅ Inserted ESG scores with ID: {score_id}")
    except Exception as e:
        print(f"❌ Error inserting ESG scores: {e}")
    
    # 3. INSERT NEWS DATA
    news_data = {
        "company_id": company_id,
        "title": "Apple Announces New Sustainability Initiative",
        "content": "Apple Inc. today announced ambitious new environmental goals...",
        "url": "https://example.com/apple-sustainability",
        "sentiment_score": 0.85,
        "source": "Reuters",
        "published_at": datetime.utcnow()
    }
    
    try:
        news_id = db.insert_news(news_data)
        print(f"✅ Inserted news with ID: {news_id}")
    except Exception as e:
        print(f"❌ Error inserting news: {e}")
    
    # 4. RETRIEVE DATA
    try:
        # Get company by ticker
        company = db.get_company_by_ticker("AAPL")
        print(f"📊 Company data: {company}")
        
        # Get latest ESG scores
        esg_scores = db.get_latest_esg_scores("AAPL")
        print(f"🌱 ESG scores: {esg_scores}")
        
        # Get recent news
        recent_news = db.get_recent_news("AAPL", limit=5)
        print(f"📰 Recent news count: {len(recent_news)}")
        
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")

def batch_data_insertion_example():
    """Example of inserting multiple companies and their ESG data."""
    
    db = DatabaseManager()
    
    # Sample data for multiple companies
    companies = [
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
        }
    ]
    
    for company_data in companies:
        try:
            company_id = db.insert_company(company_data)
            print(f"✅ Inserted {company_data['ticker']}: ID {company_id}")
            
            # Add sample ESG scores for each company
            esg_data = {
                "company_id": company_id,
                "environmental_score": 70 + (hash(company_data['ticker']) % 20),
                "social_score": 75 + (hash(company_data['ticker']) % 15),
                "governance_score": 80 + (hash(company_data['ticker']) % 10),
                "overall_score": 75 + (hash(company_data['ticker']) % 15),
                "data_source": "Sample Data"
            }
            
            score_id = db.insert_esg_scores(esg_data)
            print(f"   📊 Added ESG scores: ID {score_id}")
            
        except Exception as e:
            print(f"❌ Error with {company_data['ticker']}: {e}")

def query_examples():
    """Examples of different database queries you can perform."""
    
    db = DatabaseManager()
    
    # Using SQLAlchemy session for custom queries
    if db.SessionLocal:  # Only in development mode
        session = db.get_session()
        
        try:
            # Query companies by sector
            from src.database import Company, ESGScores
            
            tech_companies = session.query(Company).filter(
                Company.sector == "Technology"
            ).all()
            
            print(f"🏢 Technology companies: {len(tech_companies)}")
            for company in tech_companies:
                print(f"   - {company.ticker}: {company.name}")
            
            # Query companies with high ESG scores
            high_esg_companies = session.query(Company, ESGScores).join(
                ESGScores, Company.id == ESGScores.company_id
            ).filter(
                ESGScores.overall_score > 80
            ).all()
            
            print(f"🌟 High ESG score companies: {len(high_esg_companies)}")
            for company, esg in high_esg_companies:
                print(f"   - {company.ticker}: {esg.overall_score}")
                
        except Exception as e:
            print(f"❌ Query error: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    print("🗄️ PostgreSQL Database Examples for ESG Tracker")
    print("=" * 50)
    
    print("\n1. Basic Usage Example:")
    example_database_usage()
    
    print("\n2. Batch Insertion Example:")
    batch_data_insertion_example()
    
    print("\n3. Custom Query Examples:")
    query_examples()
    
    print("\n✅ Database examples completed!") 