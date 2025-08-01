# ESG Data Tracker - Troubleshooting Guide

## 🚨 Common Issues and Solutions

### 1. **"ValueError: could not convert string to float: 'None'"**
**Problem**: The Alpha Vantage API returns "None" as a string for some financial data fields.

**Solution**: ✅ **FIXED** - The code now handles "None" values properly with try-catch blocks.

### 2. **App Closes Unexpectedly**
**Problem**: Streamlit crashes due to unhandled exceptions or API errors.

**Solutions**:
- ✅ **FIXED** - Added comprehensive error handling for API calls
- ✅ **FIXED** - Added fallback to sample data when APIs fail
- ✅ **FIXED** - Increased timeout values for API requests

### 3. **"N/A" Values Showing Instead of Real Data**
**Problem**: API calls are failing or returning empty data.

**Solutions**:
- Check your internet connection
- Verify API keys are valid and not expired
- Check API rate limits (Alpha Vantage: 5 calls/minute, 500/day)
- Use the diagnostic script: `python3 diagnose_issues.py`

### 4. **Connection Error Popup**
**Problem**: Streamlit server is not running or crashed.

**Solutions**:
- Restart the dashboard: `./start_dashboard.sh`
- Check if port 8501 is available: `lsof -i :8501`
- Kill existing processes: `pkill -f streamlit`

## 🔧 Quick Fixes

### Start the Dashboard Properly
```bash
# Navigate to project directory
cd /Users/kritinkaul/automated-esg-tracker

# Activate virtual environment
source venv/bin/activate

# Run the dashboard
./start_dashboard.sh
```

### Run Diagnostics
```bash
# Check for issues
python3 diagnose_issues.py

# Test API connections
python3 -c "
import os
from dotenv import load_dotenv
import requests
load_dotenv()
# Test your APIs here
"
```

### Reset Everything
```bash
# Stop all Streamlit processes
pkill -f streamlit

# Clear browser cache
# Restart the dashboard
./start_dashboard.sh
```

## 📊 Understanding the Data Display

### When You See "N/A" Values:
1. **API Rate Limit**: Alpha Vantage has strict limits
2. **Network Issues**: Check your internet connection
3. **Invalid API Key**: Verify your keys in `.env` file
4. **API Service Down**: Check API status pages

### When You See Sample Data:
- This means the real APIs failed, but the app is still working
- Sample data shows the app structure and functionality
- Check the error messages in the dashboard for specific issues

## 🌐 API Status and Limits

### Alpha Vantage API
- **Free Tier**: 5 calls/minute, 500 calls/day
- **Rate Limit**: Wait 12 seconds between calls
- **Status**: https://www.alphavantage.co/support/

### News API
- **Free Tier**: 1,000 requests/day
- **Rate Limit**: 100 requests/hour
- **Status**: https://newsapi.org/

## 🛠️ Advanced Troubleshooting

### Check Logs
```bash
# View Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log

# Check system logs
dmesg | grep -i streamlit
```

### Debug Mode
```bash
# Run with debug logging
streamlit run main_dashboard.py --logger.level debug
```

### Test Individual Components
```bash
# Test Alpha Vantage
python3 -c "
import os
from dotenv import load_dotenv
import requests
load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
response = requests.get('https://www.alphavantage.co/query', 
                       params={'function': 'OVERVIEW', 'symbol': 'AAPL', 'apikey': api_key})
print(response.json())
"
```

## 📞 Getting Help

If you're still having issues:

1. **Run the diagnostic script**: `python3 diagnose_issues.py`
2. **Check the logs**: Look for error messages
3. **Verify API keys**: Make sure they're valid and not expired
4. **Test internet connection**: Ensure you can access external APIs
5. **Restart everything**: Stop all processes and start fresh

## 🎯 Success Indicators

When everything is working correctly, you should see:
- ✅ "Real data loaded from Alpha Vantage"
- ✅ Company information (Name, Sector, Industry)
- ✅ Financial metrics (Market Cap, P/E Ratio, Dividend Yield)
- ✅ "X real news articles loaded"
- ✅ Expandable news articles with details

## 🔄 Regular Maintenance

- **Daily**: Check if APIs are working
- **Weekly**: Verify API keys are still valid
- **Monthly**: Update dependencies: `pip install -r requirements.txt --upgrade`

---

**Last Updated**: July 28, 2024
**Version**: 1.0.0 