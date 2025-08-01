"""
Database initialization script for ESG Data Tracker.
Sets up database tables and populates with initial mock data.
"""

import logging
import sys
import os

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_db_manager, Base
from utils.mock_data import populate_mock_data
from utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize the database with tables and sample data."""
    try:
        logger.info("Initializing ESG Data Tracker database...")
        
        # Get database manager
        db_manager = get_db_manager()
        
        # Create tables (for local development)
        if settings.environment == "development":
            logger.info("Creating database tables...")
            db_manager.engine = get_db_manager().engine
            Base.metadata.create_all(bind=db_manager.engine)
            logger.info("Database tables created successfully")
        
        # Populate with mock data
        logger.info("Populating database with mock data...")
        populate_mock_data()
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def main():
    """Main function to run database initialization."""
    try:
        init_database()
        print("✅ Database initialized successfully!")
        print("You can now run the dashboard with: streamlit run dashboard/main.py")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 