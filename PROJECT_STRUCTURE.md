# Project Structure 📁

```
automated-esg-tracker/
├── 📁 src/                          # Main source code
│   ├── 📁 data_collection/          # Data collection modules
│   │   ├── yahoo_finance_collector.py    # Yahoo Finance API
│   │   ├── news_api_collector.py         # News API integration
│   │   ├── alpha_vantage_collector.py    # Alpha Vantage API
│   │   └── data_orchestrator.py          # Main orchestrator
│   ├── 📁 data_processing/          # Data processing modules
│   │   └── sentiment_analyzer.py         # AI sentiment analysis
│   ├── 📁 visualization/            # Dashboard and charts
│   │   └── main.py                       # Streamlit dashboard
│   ├── 📁 api/                      # API endpoints
│   ├── config.py                    # Configuration management
│   ├── database.py                  # Database operations
│   └── mock_data.py                 # Mock data (fallback)
├── 📁 config/                       # Configuration files
│   └── api_keys.py                  # API key management
├── 📁 logs/                         # Application logs
├── 📁 data/                         # Data storage
├── 📁 tests/                        # Unit tests
├── 📁 docs/                         # Documentation
├── 📁 .github/                      # GitHub Actions
├── 📁 .streamlit/                   # Streamlit configuration
├── .env                             # Environment variables
├── requirements.txt                 # Python dependencies
├── setup.py                         # Project setup script
├── setup_real_data.py               # Real data setup
├── test_real_data.py                # Data source testing
├── REAL_DATA_SETUP.md               # Real data guide
├── PROJECT_STRUCTURE.md             # This file
└── README.md                        # Main documentation
```

## 📊 Data Flow

```
External APIs → Data Collectors → Data Processing → Database → Dashboard
     ↓              ↓                    ↓            ↓          ↓
Yahoo Finance  → yahoo_finance_collector.py → sentiment_analyzer.py → Supabase → Streamlit
News API       → news_api_collector.py
Alpha Vantage  → alpha_vantage_collector.py
```

## 🔧 Key Components

### Data Collection (`src/data_collection/`)
- **yahoo_finance_collector.py**: Real ESG scores and company data
- **news_api_collector.py**: ESG-related news articles
- **alpha_vantage_collector.py**: Financial metrics and sentiment
- **data_orchestrator.py**: Coordinates all data collection

### Data Processing (`src/data_processing/`)
- **sentiment_analyzer.py**: AI-powered news sentiment analysis

### Visualization (`src/visualization/`)
- **main.py**: Streamlit dashboard with interactive charts

### Configuration (`config/`)
- **api_keys.py**: API key management and validation

## 🚀 Getting Started

1. **Setup**: `python setup_real_data.py`
2. **Test**: `python test_real_data.py`
3. **Run**: `streamlit run src/visualization/main.py`
4. **Collect**: `python src/data_collection/data_orchestrator.py`

## 📈 Data Sources

| Source | Purpose | Rate Limit | Cost |
|--------|---------|------------|------|
| Yahoo Finance | ESG scores, company info | None | Free |
| News API | ESG news articles | 1000/day | Free tier |
| Alpha Vantage | Financial data | 500/day | Free tier |
| Supabase | Database storage | 500MB | Free tier |

## 🔄 Automation

- **Daily Collection**: GitHub Actions workflow
- **Data Processing**: Automated sentiment analysis
- **Dashboard Updates**: Real-time data refresh
- **Error Handling**: Graceful fallbacks and retries

## 📊 Data Quality

- **Validation**: Score ranges, required fields
- **Deduplication**: Prevents duplicate articles
- **Error Recovery**: Fallback to available sources
- **Monitoring**: Comprehensive logging

## 🛡️ Security

- **API Keys**: Environment variable storage
- **Rate Limiting**: Respects API limits
- **Data Privacy**: No sensitive data collection
- **Error Handling**: Secure error messages
