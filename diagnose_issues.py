#!/usr/bin/env python3
"""
ESG Data Tracker - Issue Diagnostic Script
Helps identify and fix common problems
"""

import os
import sys
import requests
from dotenv import load_dotenv

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8+ required")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_dependencies():
    """Check required packages"""
    print("\n📦 Checking dependencies...")
    required_packages = ['streamlit', 'requests', 'pandas', 'plotly', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   💡 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    return True

def check_env_file():
    """Check environment file"""
    print("\n🔧 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        return False
    
    load_dotenv()
    
    # Check API keys
    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    
    if not alpha_key:
        print("   ❌ ALPHA_VANTAGE_API_KEY not found")
    else:
        print(f"   ✅ ALPHA_VANTAGE_API_KEY: {alpha_key[:10]}...")
    
    if not news_key:
        print("   ❌ NEWS_API_KEY not found")
    else:
        print(f"   ✅ NEWS_API_KEY: {news_key[:10]}...")
    
    return alpha_key and news_key

def test_api_connections():
    """Test API connections"""
    print("\n🌐 Testing API connections...")
    load_dotenv()
    
    # Test Alpha Vantage
    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if alpha_key:
        print("   Testing Alpha Vantage API...")
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "OVERVIEW",
                "symbol": "AAPL",
                "apikey": alpha_key
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "Error Message" not in data and "Note" not in data:
                    print("   ✅ Alpha Vantage API working")
                elif "Note" in data:
                    print(f"   ⚠️ Alpha Vantage API: {data['Note']}")
                else:
                    print("   ❌ Alpha Vantage API error")
            else:
                print(f"   ❌ Alpha Vantage API HTTP error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Alpha Vantage API connection failed: {e}")
    
    # Test News API
    news_key = os.getenv('NEWS_API_KEY')
    if news_key:
        print("   Testing News API...")
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": "ESG",
                "apiKey": news_key,
                "pageSize": 1
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    print("   ✅ News API working")
                else:
                    print(f"   ❌ News API error: {data.get('message', 'Unknown')}")
            else:
                print(f"   ❌ News API HTTP error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ News API connection failed: {e}")

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ Checking Streamlit configuration...")
    
    config_file = '.streamlit/config.toml'
    if os.path.exists(config_file):
        print("   ✅ Streamlit config file exists")
    else:
        print("   ⚠️ Streamlit config file not found (will use defaults)")

def main():
    """Run all diagnostics"""
    print("🔍 ESG Data Tracker - Issue Diagnostics")
    print("=" * 50)
    
    issues_found = []
    
    # Run all checks
    if not check_python_version():
        issues_found.append("Python version")
    
    if not check_dependencies():
        issues_found.append("Dependencies")
    
    if not check_env_file():
        issues_found.append("Environment configuration")
    
    test_api_connections()
    check_streamlit_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if issues_found:
        print(f"❌ Issues found: {', '.join(issues_found)}")
        print("\n💡 RECOMMENDATIONS:")
        print("1. Make sure you're in the virtual environment: source venv/bin/activate")
        print("2. Install missing dependencies: pip install -r requirements.txt")
        print("3. Check your .env file has valid API keys")
        print("4. Ensure you have internet connection")
        print("5. Try running: ./start_dashboard.sh")
    else:
        print("✅ No major issues detected!")
        print("\n🚀 Try running: ./start_dashboard.sh")

if __name__ == "__main__":
    main() 