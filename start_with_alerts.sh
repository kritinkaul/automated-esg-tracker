#!/bin/bash

# ESG Data Tracker with Email Alerts
# Enhanced startup script with email alert system

echo "🌱 Starting ESG Data Tracker with Email Alerts"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade required packages
echo "📦 Installing/upgrading required packages..."
pip install --upgrade pip
pip install streamlit pandas plotly requests python-dotenv yfinance

# Create data directory if it doesn't exist
mkdir -p data

# Check if email alert system is available
if [ -f "src/email_alert_system.py" ]; then
    echo "✅ Email alert system found"
    EMAIL_ALERTS_AVAILABLE=true
else
    echo "⚠️ Email alert system not found"
    EMAIL_ALERTS_AVAILABLE=false
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Environment configuration found"
else
    echo "⚠️ No .env file found. Creating basic configuration..."
    cat > .env << EOF
# ESG Data Tracker Configuration

# API Keys (add your keys here)
ALPHA_VANTAGE_KEY=demo
NEWS_API_KEY=demo
OPENWEATHER_API_KEY=demo
FINNHUB_API_KEY=demo
CARBON_INTERFACE_API_KEY=demo
NASDAQ_API_KEY=demo
FMP_API_KEY=demo

# Email Alert Configuration (configure these for email alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
FROM_NAME=ESG Data Tracker

# Environment
ENVIRONMENT=development
EOF
    echo "📝 Created .env file with default configuration"
    echo "🔧 Please edit .env file to add your API keys and email settings"
fi

# Run tests if email alerts are available
if [ "$EMAIL_ALERTS_AVAILABLE" = true ]; then
    echo "🧪 Running email alert system tests..."
    python test_email_alerts.py
    echo ""
fi

# Show available options
echo "🚀 Available Options:"
echo "1. Start main dashboard with email alerts"
echo "2. Configure email settings"
echo "3. Run email alert tests"
echo "4. Start basic dashboard (without email alerts)"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "🌱 Starting ESG Dashboard with Email Alerts..."
        streamlit run ultimate_dashboard.py
        ;;
    2)
        if [ "$EMAIL_ALERTS_AVAILABLE" = true ]; then
            echo "📧 Opening email configuration..."
            streamlit run email_setup.py
        else
            echo "❌ Email alert system not available"
        fi
        ;;
    3)
        if [ "$EMAIL_ALERTS_AVAILABLE" = true ]; then
            echo "🧪 Running email alert tests..."
            python test_email_alerts.py
        else
            echo "❌ Email alert system not available"
        fi
        ;;
    4)
        echo "🌱 Starting basic ESG Dashboard..."
        streamlit run ultimate_dashboard.py
        ;;
    *)
        echo "❌ Invalid option. Starting main dashboard..."
        streamlit run ultimate_dashboard.py
        ;;
esac 