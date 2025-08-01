#!/usr/bin/env python3
"""
Setup script for real data collection
Helps users configure API keys and test data sources
"""

import os
import sys
import requests
from typing import Dict, List, Any
import json


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_step(step: int, description: str):
    """Print a formatted step"""
    print(f"\n{step}. {description}")
    print("-" * 40)


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def test_news_api(api_key: str) -> bool:
    """Test News API connection"""
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "apiKey": api_key,
            "pageSize": 1
        }
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200
    except Exception:
        return False


def test_alpha_vantage(api_key: str) -> bool:
    """Test Alpha Vantage API connection"""
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": "AAPL",
            "interval": "1min",
            "apikey": api_key
        }
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200 and "Error Message" not in response.text
    except Exception:
        return False


def test_yahoo_finance() -> bool:
    """Test Yahoo Finance connection"""
    try:
        import yfinance as yf
        stock = yf.Ticker("AAPL")
        info = stock.info
        return "longName" in info
    except Exception:
        return False


def create_env_file(api_keys: Dict[str, str]):
    """Create or update .env file"""
    env_content = []
    
    # Add existing environment variables
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            existing_lines = f.readlines()
            for line in existing_lines:
                if not line.startswith("#") and "=" in line:
                    key = line.split("=")[0].strip()
                    if key not in api_keys:
                        env_content.append(line.strip())
    
    # Add new API keys
    env_content.append("\n# API Keys for Real Data Collection")
    for key, value in api_keys.items():
        if value:
            env_content.append(f"{key}={value}")
    
    # Write to .env file
    with open(".env", "w") as f:
        f.write("\n".join(env_content))
    
    print("✅ .env file updated with API keys")


def main():
    """Main setup function"""
    print_header("ESG Data Tracker - Real Data Setup")
    
    print("This script will help you configure API keys for real data collection.")
    print("You'll need to sign up for free accounts at the following services:")
    print("  - NewsAPI.org (free tier: 1000 requests/day)")
    print("  - Alpha Vantage (free tier: 500 requests/day)")
    print("  - Yahoo Finance (no API key required)")
    
    api_keys = {}
    
    # Step 1: News API
    print_step(1, "News API Configuration")
    print("Sign up at: https://newsapi.org/register")
    print("Free tier includes 1000 requests per day")
    
    news_api_key = get_user_input("Enter your News API key")
    if news_api_key:
        api_keys["NEWS_API_KEY"] = news_api_key
        if test_news_api(news_api_key):
            print("✅ News API connection successful!")
        else:
            print("❌ News API connection failed. Please check your key.")
    
    # Step 2: Alpha Vantage
    print_step(2, "Alpha Vantage Configuration")
    print("Sign up at: https://www.alphavantage.co/support/#api-key")
    print("Free tier includes 500 requests per day")
    
    alpha_key = get_user_input("Enter your Alpha Vantage API key")
    if alpha_key:
        api_keys["ALPHA_VANTAGE_API_KEY"] = alpha_key
        if test_alpha_vantage(alpha_key):
            print("✅ Alpha Vantage connection successful!")
        else:
            print("❌ Alpha Vantage connection failed. Please check your key.")
    
    # Step 3: Test Yahoo Finance
    print_step(3, "Testing Yahoo Finance")
    if test_yahoo_finance():
        print("✅ Yahoo Finance connection successful!")
    else:
        print("❌ Yahoo Finance connection failed. Please check your internet connection.")
    
    # Step 4: Database Configuration
    print_step(4, "Database Configuration")
    print("For Supabase (recommended):")
    print("1. Go to https://supabase.com")
    print("2. Create a free account and project")
    print("3. Get your project URL and API key")
    
    supabase_url = get_user_input("Enter your Supabase project URL")
    if supabase_url:
        api_keys["SUPABASE_URL"] = supabase_url
    
    supabase_key = get_user_input("Enter your Supabase API key")
    if supabase_key:
        api_keys["SUPABASE_KEY"] = supabase_key
    
    # Step 5: Update .env file
    print_step(5, "Updating Configuration")
    create_env_file(api_keys)
    
    # Step 6: Install dependencies
    print_step(6, "Installing Dependencies")
    print("Installing additional packages for real data collection...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
    
    # Step 7: Test data collection
    print_step(7, "Testing Data Collection")
    print("Running a test data collection...")
    
    try:
        from src.data_collection.data_orchestrator import DataOrchestrator
        
        orchestrator = DataOrchestrator()
        test_data = orchestrator.collect_company_data("AAPL", days_back=7)
        
        if test_data["company_info"]:
            print("✅ Data collection test successful!")
            print(f"   Company: {test_data['company_info']['name']}")
            print(f"   ESG Scores: {len(test_data['esg_scores'])}")
            print(f"   News Articles: {len(test_data['news'])}")
        else:
            print("❌ Data collection test failed. Check your API keys.")
            
    except Exception as e:
        print(f"❌ Error during data collection test: {e}")
    
    # Final instructions
    print_header("Setup Complete!")
    print("Your ESG Data Tracker is now configured for real data collection!")
    print("\nNext steps:")
    print("1. Run the dashboard: streamlit run src/visualization/main.py")
    print("2. Collect data: python src/data_collection/data_orchestrator.py")
    print("3. Check the logs folder for any errors")
    print("\nAvailable data sources:")
    for key, value in api_keys.items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}")
    
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
