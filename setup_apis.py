#!/usr/bin/env python3
"""
API Setup Script for ESG Tracker
Helps you configure free APIs for enhanced features
"""

import os
import requests
import json
from datetime import datetime

def check_api_key(api_name, api_key, test_url, test_params=None):
    """Test if an API key is working"""
    try:
        if test_params:
            response = requests.get(test_url, params=test_params, timeout=10)
        else:
            response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {api_name} API key is working!")
            return True
        else:
            print(f"❌ {api_name} API key failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {api_name} API test failed: {e}")
        return False

def setup_environment():
    """Set up environment variables for APIs"""
    print("🚀 Setting up API keys for ESG Tracker...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# API Keys for ESG Tracker\n")
            f.write("# Add your API keys here\n\n")
    
    # Read existing .env file
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value
    
    # API configuration
    apis = {
        "ALPHA_VANTAGE_KEY": {
            "name": "Alpha Vantage",
            "url": "https://www.alphavantage.co/support/#api-key",
            "test_url": "https://www.alphavantage.co/query",
            "test_params": {"function": "TIME_SERIES_INTRADAY", "symbol": "AAPL", "interval": "1min", "apikey": ""},
            "description": "Stock data and technical indicators"
        },
        "NEWS_API_KEY": {
            "name": "NewsAPI",
            "url": "https://newsapi.org/register",
            "test_url": "https://newsapi.org/v2/top-headlines",
            "test_params": {"country": "us", "apiKey": ""},
            "description": "News articles and sentiment analysis"
        },
        "OPENWEATHER_API_KEY": {
            "name": "OpenWeatherMap",
            "url": "https://openweathermap.org/api",
            "test_url": "http://api.openweathermap.org/data/2.5/weather",
            "test_params": {"q": "London", "appid": ""},
            "description": "Weather data and climate information"
        },
        "FINNHUB_API_KEY": {
            "name": "Finnhub",
            "url": "https://finnhub.io/register",
            "test_url": "https://finnhub.io/api/v1/quote",
            "test_params": {"symbol": "AAPL", "token": ""},
            "description": "Real-time financial data"
        },
        "HUGGINGFACE_API_KEY": {
            "name": "Hugging Face",
            "url": "https://huggingface.co/settings/tokens",
            "test_url": "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest",
            "test_params": None,
            "description": "AI sentiment analysis"
        }
    }
    
    print("📋 Available APIs to configure:")
    for i, (key, api) in enumerate(apis.items(), 1):
        status = "✅ Configured" if env_vars.get(key) else "❌ Not configured"
        print(f"{i}. {api['name']} - {status}")
        print(f"   Description: {api['description']}")
        print(f"   Get API key: {api['url']}")
        print()
    
    # Interactive setup
    print("🔧 Let's configure your APIs:")
    print("Enter 'skip' to skip any API, or 'test' to test existing keys")
    
    for key, api in apis.items():
        current_key = env_vars.get(key, "")
        
        if current_key:
            print(f"\n🔑 {api['name']} already configured")
            action = input("Test existing key? (y/n/skip): ").lower()
            
            if action == "y":
                # Test the existing key
                test_params = api['test_params'].copy() if api['test_params'] else {}
                if test_params:
                    test_params[list(test_params.keys())[-1]] = current_key
                    check_api_key(api['name'], current_key, api['test_url'], test_params)
            elif action == "skip":
                continue
        else:
            print(f"\n🔑 {api['name']} - {api['description']}")
            print(f"Get your free API key at: {api['url']}")
            
            new_key = input(f"Enter your {api['name']} API key (or 'skip'): ").strip()
            
            if new_key.lower() == "skip":
                continue
            elif new_key:
                env_vars[key] = new_key
                
                # Test the new key
                test_params = api['test_params'].copy() if api['test_params'] else {}
                if test_params:
                    test_params[list(test_params.keys())[-1]] = new_key
                    check_api_key(api['name'], new_key, api['test_url'], test_params)
    
    # Write updated .env file
    print("\n💾 Saving API keys to .env file...")
    with open(env_file, "w") as f:
        f.write("# API Keys for ESG Tracker\n")
        f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Environment setup complete!")
    print("\n🎯 Next steps:")
    print("1. Run: streamlit run ultimate_dashboard.py")
    print("2. Test the enhanced features")
    print("3. Check the FREE_APIS_GUIDE.md for more APIs")

def test_all_apis():
    """Test all configured APIs"""
    print("🧪 Testing all configured APIs...")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    apis_to_test = {
        "Alpha Vantage": {
            "key": os.getenv("ALPHA_VANTAGE_KEY"),
            "test_url": "https://www.alphavantage.co/query",
            "test_params": {"function": "TIME_SERIES_INTRADAY", "symbol": "AAPL", "interval": "1min", "apikey": ""}
        },
        "NewsAPI": {
            "key": os.getenv("NEWS_API_KEY"),
            "test_url": "https://newsapi.org/v2/top-headlines",
            "test_params": {"country": "us", "apiKey": ""}
        },
        "OpenWeatherMap": {
            "key": os.getenv("OPENWEATHER_API_KEY"),
            "test_url": "http://api.openweathermap.org/data/2.5/weather",
            "test_params": {"q": "London", "appid": ""}
        },
        "Finnhub": {
            "key": os.getenv("FINNHUB_API_KEY"),
            "test_url": "https://finnhub.io/api/v1/quote",
            "test_params": {"symbol": "AAPL", "token": ""}
        }
    }
    
    results = {}
    for name, config in apis_to_test.items():
        if config["key"]:
            test_params = config["test_params"].copy()
            test_params[list(test_params.keys())[-1]] = config["key"]
            
            success = check_api_key(name, config["key"], config["test_url"], test_params)
            results[name] = success
        else:
            print(f"❌ {name}: No API key configured")
            results[name] = False
    
    # Summary
    print("\n📊 API Test Summary:")
    working_apis = sum(results.values())
    total_apis = len(results)
    
    for name, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"   {name}: {status}")
    
    print(f"\n🎯 {working_apis}/{total_apis} APIs are working")
    
    if working_apis > 0:
        print("🚀 Your ESG tracker is ready with real data!")
    else:
        print("⚠️  No APIs are working. Please check your API keys.")

if __name__ == "__main__":
    print("🌱 ESG Tracker API Setup")
    print("=" * 30)
    
    action = input("Choose action:\n1. Setup new APIs\n2. Test existing APIs\nEnter choice (1/2): ")
    
    if action == "1":
        setup_environment()
    elif action == "2":
        test_all_apis()
    else:
        print("Invalid choice. Running setup...")
        setup_environment() 