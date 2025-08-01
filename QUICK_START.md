# 🚀 Quick Start Guide

## ✅ Your ESG Data Tracker is Ready!

### 📍 **Important: Always run commands from the project directory**

You must be in: `/Users/kritinkaul/automated-esg-tracker`

## 🎯 **How to Run Everything**

### Option 1: Use the Interactive Menu (Recommended)
```bash
cd /Users/kritinkaul/automated-esg-tracker
python3 run_esg_tracker.py
```

This gives you a menu with options:
- 🚀 Start Dashboard
- 📊 Collect Real Data  
- 📋 Show Current Data
- 🧪 Test APIs

### Option 2: Direct Commands

**1. Start the Dashboard:**
```bash
cd /Users/kritinkaul/automated-esg-tracker
streamlit run src/visualization/main.py
```

**2. Collect Real Data:**
```bash
cd /Users/kritinkaul/automated-esg-tracker
python3 collect_real_data.py
```

**3. Show Current Data:**
```bash
cd /Users/kritinkaul/automated-esg-tracker
python3 show_real_data.py
```

**4. Test APIs:**
```bash
cd /Users/kritinkaul/automated-esg-tracker
python3 test_real_data.py
```

## 🔧 **If Dashboard Port is Busy**

If you get "Port 8501 is already in use":

**Option A: Use a different port**
```bash
streamlit run src/visualization/main.py --server.port 8502
```

**Option B: Kill existing process**
```bash
lsof -ti:8501 | xargs kill -9
streamlit run src/visualization/main.py
```

## 📊 **What You're Getting**

✅ **Real ESG News** from News API (Forbes, GlobeNewswire)
✅ **Real Financial Data** from Alpha Vantage (Apple Inc., $3.2T market cap)
✅ **AI Sentiment Analysis** of news articles
✅ **Professional Dashboard** with interactive charts

## 🎉 **You're Collecting Real Data!**

- No more mock data
- Real news articles about ESG
- Real company financial information
- Real sentiment analysis

## 📞 **Need Help?**

1. **Always check your directory first:**
   ```bash
   pwd
   # Should show: /Users/kritinkaul/automated-esg-tracker
   ```

2. **Check if files exist:**
   ```bash
   ls -la collect_real_data.py
   ls -la src/visualization/main.py
   ```

3. **Use the interactive menu:**
   ```bash
   python3 run_esg_tracker.py
   ```

---

**🎯 Start with: `python3 run_esg_tracker.py`**
