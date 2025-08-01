#!/usr/bin/env python3
"""
ESG Data Tracker - Main Runner Script
Handles all common tasks and provides easy navigation
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_directory():
    """Check if we're in the correct directory"""
    required_files = ["collect_real_data.py", "src/visualization/main.py"]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Error: {file} not found")
            print(f"   Current directory: {os.getcwd()}")
            print(f"   Please run this script from the automated-esg-tracker directory")
            return False
    
    print("✅ Directory check passed")
    return True

def run_dashboard():
    """Run the Streamlit dashboard"""
    print_header("Starting ESG Data Tracker Dashboard")
    
    if not check_directory():
        return
    
    try:
        print("🚀 Starting Streamlit dashboard...")
        print("   Dashboard will open in your browser at: http://localhost:8501")
        print("   Press Ctrl+C to stop the dashboard")
        print()
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/visualization/main.py", "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

def collect_data():
    """Collect real ESG data"""
    print_header("Collecting Real ESG Data")
    
    if not check_directory():
        return
    
    try:
        print("📊 Collecting data from multiple sources...")
        subprocess.run([sys.executable, "collect_real_data.py"])
    except Exception as e:
        print(f"❌ Error collecting data: {e}")

def show_data():
    """Show current real data"""
    print_header("Showing Real Data Sources")
    
    if not check_directory():
        return
    
    try:
        subprocess.run([sys.executable, "show_real_data.py"])
    except Exception as e:
        print(f"❌ Error showing data: {e}")

def test_apis():
    """Test API connections"""
    print_header("Testing API Connections")
    
    if not check_directory():
        return
    
    try:
        subprocess.run([sys.executable, "test_real_data.py"])
    except Exception as e:
        print(f"❌ Error testing APIs: {e}")

def main():
    """Main menu"""
    while True:
        print_header("ESG Data Tracker - Main Menu")
        print("Choose an option:")
        print("1. 🚀 Start Dashboard")
        print("2. 📊 Collect Real Data")
        print("3. 📋 Show Current Data")
        print("4. 🧪 Test APIs")
        print("5. 📁 Show Project Structure")
        print("6. ❓ Help")
        print("0. 🚪 Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "1":
            run_dashboard()
        elif choice == "2":
            collect_data()
        elif choice == "3":
            show_data()
        elif choice == "4":
            test_apis()
        elif choice == "5":
            show_project_structure()
        elif choice == "6":
            show_help()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 0-6.")

def show_project_structure():
    """Show project structure"""
    print_header("Project Structure")
    
    structure = """
📁 automated-esg-tracker/
├── 📁 src/
│   ├── 📁 data_collection/     # Real data collectors
│   │   ├── yahoo_finance_collector.py
│   │   ├── news_api_collector.py
│   │   ├── alpha_vantage_collector.py
│   │   └── data_orchestrator.py
│   ├── 📁 data_processing/     # AI sentiment analysis
│   │   └── sentiment_analyzer.py
│   └── 📁 visualization/       # Dashboard
│       └── main.py
├── 📁 config/                  # API configuration
├── .env                        # Your API keys
├── collect_real_data.py        # Data collection
├── show_real_data.py          # Data verification
├── test_real_data.py          # API testing
└── run_esg_tracker.py         # This script
"""
    print(structure)

def show_help():
    """Show help information"""
    print_header("Help & Troubleshooting")
    
    help_text = """
🚀 Quick Start:
1. Choose option 1 to start the dashboard
2. Choose option 2 to collect real data
3. Choose option 3 to see what data you have

📊 Data Sources:
- News API: Real ESG news articles
- Alpha Vantage: Financial data & sentiment
- AI Analysis: Sentiment analysis of news

🔧 Common Issues:
- If dashboard doesn't start: Check if port 8501 is free
- If data collection fails: Check API rate limits
- If files not found: Make sure you're in the right directory

📁 Directory Structure:
Make sure you're in: /Users/kritinkaul/automated-esg-tracker

🔑 API Keys:
Your keys are configured in .env file:
- News API: ✅ Working
- Alpha Vantage: ✅ Working
- Supabase: ✅ Configured

📞 Need More Help?
Check these files:
- SETUP_COMPLETE.md
- REAL_DATA_SETUP.md
- README.md
"""
    print(help_text)

if __name__ == "__main__":
    main()
