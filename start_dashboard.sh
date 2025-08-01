#!/bin/bash

# ESG Data Tracker Dashboard Startup Script

echo "🌱 Starting ESG Data Tracker Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please check your configuration."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import streamlit, requests, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Please run: pip install -r requirements.txt"
    exit 1
fi

# Start the dashboard
echo "🚀 Starting Streamlit dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

streamlit run main_dashboard.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless true \
    --browser.gatherUsageStats false \
    --logger.level info 