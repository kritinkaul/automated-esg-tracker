# 🌱 ESG Data Tracker Ultimate

A comprehensive, real-time ESG (Environmental, Social, Governance) data tracking dashboard built with Streamlit, featuring advanced analytics, email alerts, and multi-source data integration.

🚀Live Demo: https://esgtracker.streamlit.app/

## 🚀 Features

### 📊 **Real-Time Data Integration**
- **Stock Data**: Alpha Vantage & Financial Modeling Prep APIs
- **Weather Data**: OpenWeatherMap API with 300+ global cities
- **ESG Scores**: MSCI ESG, Sustainalytics, and custom analytics
- **News & Sentiment**: Real-time ESG news with sentiment analysis
- **Environmental Data**: EPA compliance and carbon footprint tracking

### 🎯 **Advanced Analytics**
- Interactive stock price charts with technical indicators
- ESG score breakdowns and trend analysis
- Company comparison tools
- Weather impact correlation analysis
- Real-time news sentiment tracking

### 📧 **Email Alert System**
- Configurable alert thresholds
- Multiple alert types (Price, ESG, Weather, News)
- Real-time and digest email formats
- Professional HTML email templates

### 🌍 **Global Coverage**
- 300+ major cities worldwide for weather data
- International stock markets
- Multi-language support for global ESG data

## 🛠️ Installation

### Prerequisites
```bash
Python 3.8+
pip
```

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/automated-esg-tracker.git
cd automated-esg-tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Keys**
Create a `.env` file in the root directory:
```env
# Required API Keys
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
FMP_API_KEY=your_fmp_api_key
OPENWEATHER_API_KEY=your_openweather_key

# Optional API Keys
NEWS_API_KEY=your_news_api_key
CARBON_INTERFACE_API_KEY=your_carbon_key
NASDAQ_API_KEY=your_nasdaq_key
```

4. **Run the dashboard**
```bash
streamlit run ultimate_dashboard.py --server.port 8501
```

5. **Access the dashboard**
Open your browser and go to: `http://localhost:8501`

## 📊 Data Sources

### Financial Data
- **Alpha Vantage**: Historical stock data, company overviews (500 calls/day)
- **Financial Modeling Prep**: Real-time stock prices, company profiles (250 calls/day)
- **Yahoo Finance**: Backup stock data and market information

### ESG & Sustainability
- **MSCI ESG**: Environmental, Social, Governance ratings
- **Sustainalytics**: ESG risk ratings and scores
- **ESG Analytics**: Custom ESG assessments
- **Carbon Interface**: Carbon footprint calculations

### Environmental Data
- **OpenWeatherMap**: Real-time weather conditions
- **EPA Envirofacts**: Environmental compliance data
- **NASDAQ**: Market and environmental data
- **News API**: ESG-related news and updates

## 🎯 Usage Guide

### Main Dashboard
1. **Select Company**: Choose from popular stocks or enter custom symbol
2. **View Analytics**: Interactive charts with real-time data
3. **Monitor ESG**: Track environmental, social, and governance scores
4. **Weather Integration**: See how climate data correlates with performance

### Email Alerts
1. **Configure Settings**: Enter email and set preferences
2. **Set Thresholds**: Define alert triggers for price/ESG changes
3. **Choose Frequency**: Daily, weekly, monthly, or real-time alerts
4. **Test System**: Use test buttons to verify functionality

### Company Comparison
1. **Select Two Companies**: Choose different stocks to compare
2. **View Side-by-Side**: Compare performance, ESG scores, and metrics
3. **Export Data**: Download comparison reports

## 🔧 Configuration

### API Rate Limits
- Alpha Vantage: 500 calls per day
- Financial Modeling Prep: 250 calls per day
- OpenWeatherMap: 1000 calls per day
- News API: 1000 calls per day

### Data Update Frequencies
- Stock prices: Every 5 minutes during market hours
- Weather data: Every 10 minutes
- News updates: Every 30 minutes
- ESG scores: Daily updates

## 📁 Project Structure

```
automated-esg-tracker/
├── ultimate_dashboard.py      # Main dashboard application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .env                      # API keys (create this)
├── src/
│   ├── api/                  # API integration modules
│   ├── data_collection/      # Data collection scripts
│   ├── data_processing/      # Data processing utilities
│   ├── email_alert_system.py # Email alert functionality
│   └── visualization/        # Chart and visualization modules
├── data/                     # Data storage
├── logs/                     # Application logs
└── tests/                    # Test files
```

## 🚀 Deployment

### Local Development
```bash
streamlit run ultimate_dashboard.py --server.port 8501
```

### Production Deployment
1. Set up a cloud server (AWS, Google Cloud, etc.)
2. Install dependencies
3. Configure environment variables
4. Run with process manager (PM2, systemd)
5. Set up reverse proxy (nginx)

### Docker Deployment
```bash
docker build -t esg-dashboard .
docker run -p 8501:8501 esg-dashboard
```

## 🔒 Security

- API keys stored in environment variables
- Rate limiting to prevent API abuse
- Input validation and sanitization
- Secure email configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Alpha Vantage**: Financial data API
- **Financial Modeling Prep**: Real-time market data
- **OpenWeatherMap**: Weather data services
- **MSCI & Sustainalytics**: ESG rating providers
- **Streamlit**: Web application framework

## 📞 Support

For support, email support@esg-tracker.com or create an issue in this repository.

---

**Built with ❤️ for sustainable investing and ESG transparency** 
