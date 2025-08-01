# Real Data Setup Guide 🚀

This guide will help you replace mock data with real ESG data from multiple sources.

## 📋 What You'll Get

With real data sources, you'll have access to:

- **Real ESG Scores**: Actual environmental, social, and governance scores
- **Live News**: ESG-related news with sentiment analysis
- **Financial Data**: Stock prices, market cap, and financial metrics
- **Company Information**: Real company profiles and descriptions

## 🔑 Required API Keys

### 1. News API (Free Tier: 1000 requests/day)
**Purpose**: ESG-related news articles
**Sign up**: https://newsapi.org/register
**Cost**: Free tier available

### 2. Alpha Vantage (Free Tier: 500 requests/day)
**Purpose**: Financial data and sentiment analysis
**Sign up**: https://www.alphavantage.co/support/#api-key
**Cost**: Free tier available

### 3. Yahoo Finance (No API Key Required)
**Purpose**: Stock data and basic company info
**Sign up**: Not required
**Cost**: Free

### 4. Supabase (Free Tier Available)
**Purpose**: Database storage
**Sign up**: https://supabase.com
**Cost**: Free tier available

## 🛠️ Quick Setup

### Option 1: Automated Setup
```bash
python setup_real_data.py
```

### Option 2: Manual Setup

1. **Get API Keys**
   - Sign up for the services above
   - Copy your API keys

2. **Update .env file**
   ```bash
   # Add these to your .env file
   NEWS_API_KEY=your_news_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_key_here
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test Data Collection**
   ```bash
   python src/data_collection/data_orchestrator.py
   ```

## 📊 Data Sources Overview

### Yahoo Finance
- **ESG Scores**: Environmental, social, governance scores
- **Company Info**: Name, sector, industry, market cap
- **News**: Company-related news articles
- **Financial Data**: Stock prices and volumes

### News API
- **ESG News**: Articles about sustainability, governance, social responsibility
- **Keyword Filtering**: Focuses on ESG-related content
- **Multiple Sources**: Various news outlets

### Alpha Vantage
- **Company Overview**: Detailed company information
- **Sentiment Analysis**: News sentiment scores
- **Financial Metrics**: Additional financial data

## 🔄 Data Collection Process

1. **Company Information**: Fetched from Yahoo Finance and Alpha Vantage
2. **ESG Scores**: Retrieved from Yahoo Finance sustainability data
3. **News Collection**: Gathered from Yahoo Finance and News API
4. **Sentiment Analysis**: AI-powered analysis of news content
5. **Database Storage**: All data stored in Supabase PostgreSQL

## 📈 Sample Data Structure

### ESG Scores
```json
{
  "date": "2024-01-15",
  "environmental_score": 75.5,
  "social_score": 82.3,
  "governance_score": 78.9,
  "overall_score": 78.9,
  "data_source": "yahoo_finance"
}
```

### News Articles
```json
{
  "date": "2024-01-15T10:30:00",
  "headline": "Apple Announces New Renewable Energy Initiative",
  "content": "Apple has committed to...",
  "source": "Reuters",
  "url": "https://...",
  "sentiment_score": 0.8,
  "sentiment_label": "positive",
  "data_source": "news_api"
}
```

## 🚀 Running with Real Data

### Start the Dashboard
```bash
streamlit run src/visualization/main.py
```

### Collect Data
```bash
python src/data_collection/data_orchestrator.py
```

### Schedule Daily Collection
```bash
# Add to crontab for daily collection
0 9 * * * cd /path/to/project && python src/data_collection/data_orchestrator.py
```

## 🔍 Monitoring and Logs

- **Logs**: Check the `logs/` folder for detailed logs
- **Database**: Monitor data in your Supabase dashboard
- **API Usage**: Track API usage in respective service dashboards

## 🛡️ Error Handling

The system includes robust error handling:
- **API Failures**: Graceful fallback to available data sources
- **Rate Limiting**: Respects API rate limits
- **Data Validation**: Ensures data quality before storage
- **Retry Logic**: Automatic retries for failed requests

## 📊 Data Quality

### Validation Rules
- ESG scores: 0-100 range
- Sentiment scores: -1 to 1 range
- Required fields: date, source, ticker
- Duplicate detection: Prevents duplicate articles

### Data Sources Priority
1. Yahoo Finance (primary ESG data)
2. News API (supplementary news)
3. Alpha Vantage (financial metrics)
4. Mock data (fallback only)

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API keys in .env file
   - Check API key validity in service dashboards
   - Ensure you haven't exceeded rate limits

2. **No ESG Data**
   - Some companies may not have ESG data available
   - Check Yahoo Finance for company sustainability data
   - Consider using alternative data sources

3. **Database Connection Issues**
   - Verify Supabase credentials
   - Check database schema matches expectations
   - Ensure proper network connectivity

### Getting Help

1. Check the logs in `logs/` folder
2. Verify API keys are working
3. Test individual data collectors
4. Check database connection

## 📈 Performance Tips

1. **Rate Limiting**: Respect API rate limits
2. **Caching**: Implement caching for frequently accessed data
3. **Batch Processing**: Collect data in batches
4. **Error Recovery**: Implement retry logic for failed requests

## 🔄 Migration from Mock Data

If you're currently using mock data:

1. **Backup**: Backup your current database
2. **Test**: Run setup script to test real data sources
3. **Migrate**: Gradually replace mock data with real data
4. **Validate**: Ensure data quality and consistency

## 📞 Support

For issues with:
- **API Services**: Contact respective service support
- **Code Issues**: Check GitHub issues or create new one
- **Configuration**: Review this guide and setup script

---

**Happy data collecting! 🎉**
