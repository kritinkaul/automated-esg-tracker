# 🚀 Getting Started with Real Data

## Quick Start (5 minutes)

### 1. Run the Setup Script
```bash
python setup_real_data.py
```

This will:
- Guide you through getting API keys
- Test all data sources
- Update your configuration
- Install dependencies

### 2. Get Free API Keys

**News API** (1000 requests/day free):
1. Go to https://newsapi.org/register
2. Sign up for free account
3. Copy your API key

**Alpha Vantage** (500 requests/day free):
1. Go to https://www.alphavantage.co/support/#api-key
2. Sign up for free account
3. Copy your API key

**Supabase** (free database):
1. Go to https://supabase.com
2. Create free account and project
3. Get project URL and API key

### 3. Test Everything
```bash
python test_real_data.py
```

### 4. Start Collecting Real Data
```bash
python src/data_collection/data_orchestrator.py
```

### 5. Run the Dashboard
```bash
streamlit run src/visualization/main.py
```

## What You'll Get

✅ **Real ESG Scores** from Yahoo Finance
✅ **Live News Articles** with AI sentiment analysis
✅ **Financial Data** from multiple sources
✅ **Company Information** with real profiles
✅ **Automated Data Collection** daily
✅ **Interactive Dashboard** with real-time data

## Data Sources

| Source | What You Get | Rate Limit | Cost |
|--------|-------------|------------|------|
| Yahoo Finance | ESG scores, company info, news | Unlimited | Free |
| News API | ESG-related news articles | 1000/day | Free |
| Alpha Vantage | Financial metrics, sentiment | 500/day | Free |
| Supabase | Database storage | 500MB | Free |

## Project Structure

```
📁 src/
├── 📁 data_collection/     # Real data collectors
├── 📁 data_processing/     # AI sentiment analysis
├── 📁 visualization/       # Dashboard
└── 📁 api/                # API endpoints

📁 config/                 # API keys & settings
📁 logs/                   # Application logs
📁 data/                   # Data storage
```

## Next Steps

1. **Run setup script** to configure everything
2. **Get API keys** from the free services
3. **Test data collection** to verify everything works
4. **Start the dashboard** to see real data
5. **Schedule daily collection** for continuous updates

## Need Help?

- Check `REAL_DATA_SETUP.md` for detailed instructions
- Run `python test_real_data.py` to diagnose issues
- Check the `logs/` folder for error details
- Review `PROJECT_STRUCTURE.md` for architecture details

---

**You're ready to collect real ESG data! 🎉**
