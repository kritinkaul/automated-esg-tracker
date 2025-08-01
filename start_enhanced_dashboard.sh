#!/bin/bash

# Enhanced ESG Data Tracker Dashboard Startup Script

echo "🌟 Starting Enhanced ESG Data Tracker Pro..."

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
echo "🔍 Checking enhanced dependencies..."
python -c "import streamlit, requests, pandas, plotly, yfinance, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing enhanced packages..."
    pip install yfinance streamlit-option-menu streamlit-aggrid
fi

# Check if enhanced dashboard exists
if [ ! -f "enhanced_dashboard.py" ]; then
    echo "❌ Enhanced dashboard not found. Please check the file exists."
    exit 1
fi

# Display available features
echo ""
echo "🎯 Enhanced Features Available:"
echo "   📊 Interactive Stock Charts (Yahoo Finance)"
echo "   🌤️ Weather Data Integration (OpenWeatherMap)"
echo "   🌍 Carbon Footprint Calculator"
echo "   😊 Sentiment Analysis"
echo "   📈 Real-time Market Data"
echo "   🎨 Beautiful UI Components"
echo ""

# Start the enhanced dashboard
echo "🚀 Starting Enhanced Streamlit Dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

streamlit run enhanced_dashboard.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless true \
    --browser.gatherUsageStats false \
    --logger.level info 