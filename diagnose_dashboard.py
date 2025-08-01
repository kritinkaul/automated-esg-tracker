#!/usr/bin/env python3
"""
Dashboard Diagnostic Tool
Check what data is being loaded and displayed
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def diagnose_dashboard():
    """Run comprehensive dashboard diagnostics"""
    
    print("🔍 ESG Dashboard Diagnostic Report")
    print("=" * 50)
    
    # Check environment setup
    print("\n📊 Environment Check:")
    required_vars = ['NEWS_API_KEY', 'ALPHA_VANTAGE_API_KEY', 'OPENWEATHER_API_KEY']
    for var in required_vars:
        value = os.getenv(var)
        status = "✅ Set" if value else "❌ Missing"
        print(f"   {var}: {status}")
    
    # Test imports
    print("\n📦 Package Import Check:")
    packages = {
        'streamlit': 'st',
        'pandas': 'pd', 
        'plotly': 'plotly',
        'requests': 'requests',
        'yfinance': 'yf',
        'numpy': 'np'
    }
    
    for package, alias in packages.items():
        try:
            exec(f"import {package} as {alias}")
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
    
    # Test API connections (quick test)
    print("\n🌐 API Connection Check:")
    
    # Test News API
    news_key = os.getenv('NEWS_API_KEY')
    if news_key:
        try:
            import requests
            url = f"https://newsapi.org/v2/everything?q=test&apiKey={news_key}&pageSize=1"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("   ✅ News API - Working")
            else:
                print(f"   ⚠️ News API - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ News API - Error: {str(e)[:50]}...")
    else:
        print("   ❌ News API - No key")
    
    # Test OpenWeather API
    weather_key = os.getenv('OPENWEATHER_API_KEY')
    if weather_key:
        try:
            import requests
            url = f"http://api.openweathermap.org/data/2.5/weather?q=New York&appid={weather_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("   ✅ OpenWeather API - Working")
            else:
                print(f"   ⚠️ OpenWeather API - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ OpenWeather API - Error: {str(e)[:50]}...")
    else:
        print("   ❌ OpenWeather API - No key")
    
    # Test Alpha Vantage (might hit rate limit)
    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if alpha_key:
        print("   ⚠️ Alpha Vantage API - May hit rate limit (fallback available)")
    else:
        print("   ❌ Alpha Vantage API - No key")
    
    # Test dashboard functions
    print("\n🧪 Dashboard Function Check:")
    
    try:
        sys.path.append('.')
        from ultimate_dashboard import (
            get_alpha_vantage_data, 
            get_real_esg_scores, 
            get_real_carbon_footprint,
            get_real_weather_data,
            get_stock_data
        )
        
        # Test each function
        functions_to_test = [
            ('Alpha Vantage Data', lambda: get_alpha_vantage_data('AAPL')),
            ('ESG Scores', lambda: get_real_esg_scores('AAPL')),
            ('Carbon Footprint', lambda: get_real_carbon_footprint('AAPL', 'TECHNOLOGY')),
            ('Weather Data', lambda: get_real_weather_data('New York')),
            ('Stock Data', lambda: get_stock_data('AAPL'))
        ]
        
        for name, func in functions_to_test:
            try:
                result = func()
                if result:
                    print(f"   ✅ {name} - Working")
                else:
                    print(f"   ⚠️ {name} - No data returned")
            except Exception as e:
                print(f"   ❌ {name} - Error: {str(e)[:50]}...")
                
    except ImportError as e:
        print(f"   ❌ Cannot import dashboard functions: {e}")
    
    # Check common issues
    print("\n🔧 Common Issues Check:")
    
    # Check if streamlit is running
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'streamlit' in result.stdout:
            print("   ✅ Streamlit is running")
        else:
            print("   ❌ Streamlit not found in running processes")
    except:
        print("   ⚠️ Cannot check if Streamlit is running")
    
    # Final recommendations
    print("\n💡 Recommendations:")
    print("   1. If API data is missing, fallback data should still show")
    print("   2. Check browser console for JavaScript errors")
    print("   3. Refresh the dashboard page (Ctrl+F5)")
    print("   4. Check sidebar settings - some features might be disabled")
    print("   5. If charts are still missing, restart Streamlit")
    
    print("\n✅ Diagnostic Complete!")
    print("=" * 50)

if __name__ == "__main__":
    diagnose_dashboard()
