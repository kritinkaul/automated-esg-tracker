#!/bin/bash

# ESG Data Tracker Pro - Professional Dashboard Startup Script

echo "🌟 Starting ESG Data Tracker Pro - Professional Edition..."

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
echo "🔍 Checking professional dependencies..."
python -c "import streamlit, requests, pandas, plotly, yfinance, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing professional packages..."
    pip install yfinance streamlit-option-menu streamlit-aggrid
fi

# Check if pro dashboard exists
if [ ! -f "pro_dashboard.py" ]; then
    echo "❌ Professional dashboard not found. Please check the file exists."
    exit 1
fi

# Display available features
echo ""
echo "🎯 Professional Features Available:"
echo "   🌤️ Real Weather Data (OpenWeatherMap API)"
echo "   🌍 Real Carbon Footprint (Carbon Interface API)"
echo "   📊 Nasdaq ESG Data (Nasdaq API)"
echo "   😊 AI Sentiment Analysis (Hugging Face)"
echo "   📈 Interactive Stock Charts (Yahoo Finance)"
echo "   🎨 Professional UI Components"
echo "   🔌 API Status Monitoring"
echo ""

# Start the professional dashboard
echo "🚀 Starting Professional Streamlit Dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

streamlit run pro_dashboard.py \
    --server.port 8501 \
    --server.address localhost \
    --server.headless true \
    --browser.gatherUsageStats false \
    --logger.level info 