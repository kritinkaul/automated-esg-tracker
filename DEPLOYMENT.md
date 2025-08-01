# Deployment Guide for ESG Data Tracker

This guide will help you deploy your ESG Data Tracker to Streamlit Cloud for free.

## 🚀 Quick Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

### Step 1: Push to GitHub

1. **Create a new GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ESG Data Tracker"
   git branch -M main
   git remote add origin https://github.com/yourusername/automated-esg-tracker.git
   git push -u origin main
   ```

2. **Set up GitHub Secrets** (for production data collection)
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase anon key
     - `YAHOO_FINANCE_API_KEY`: Your Yahoo Finance API key (optional)
     - `NEWS_API_KEY`: Your News API key (optional)

### Step 2: Deploy to Streamlit Cloud

1. **Sign up for Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign up with your GitHub account

2. **Deploy your app**
   - Click "New app"
   - Select your GitHub repository
   - Set the main file path to: `dashboard/main.py`
   - Click "Deploy"

3. **Configure environment variables**
   - In your Streamlit Cloud app settings
   - Add the same environment variables as GitHub secrets
   - Set `ENVIRONMENT=production`

### Step 3: Set up Supabase (Optional for Production)

1. **Create a Supabase account**
   - Visit https://supabase.com
   - Sign up for free tier

2. **Create a new project**
   - Click "New project"
   - Choose a name and database password
   - Select a region close to you

3. **Get your credentials**
   - Go to Settings → API
   - Copy your project URL and anon key
   - Add these to your environment variables

## 🔧 Local Development Setup

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/automated-esg-tracker.git
cd automated-esg-tracker

# Run the setup script
python setup.py

# Start the dashboard
streamlit run dashboard/main.py
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_database.py

# Run the dashboard
streamlit run dashboard/main.py
```

## 📊 Data Sources Configuration

### Free APIs for ESG Data

1. **Yahoo Finance** (Free)
   - Provides basic company information
   - No API key required for basic usage

2. **Alpha Vantage** (Free tier)
   - Financial data and news
   - 500 requests per day free

3. **News API** (Free tier)
   - News articles and headlines
   - 100 requests per day free

4. **ESG Book** (Free tier)
   - ESG scores and metrics
   - Limited free access

### Mock Data (Development)
- The project includes realistic mock data for development
- No API keys required for testing
- Perfect for portfolio demonstrations

## 🔄 Automation Setup

### GitHub Actions
The project includes automated data collection via GitHub Actions:

1. **Daily Collection**: Runs every day at 6 AM UTC
2. **Manual Trigger**: Can be triggered manually from Actions tab
3. **Error Handling**: Logs failures and provides retry options

### Customization
Edit `.github/workflows/data_collection.yml` to:
- Change collection frequency
- Add more data sources
- Configure notifications

## 🎯 Production Considerations

### Scaling
- **Free Tier Limits**: Be aware of API rate limits
- **Database**: Supabase free tier includes 500MB storage
- **Streamlit Cloud**: Free tier includes 1GB RAM

### Security
- Never commit API keys to Git
- Use environment variables for all secrets
- Regularly rotate API keys

### Monitoring
- Check GitHub Actions logs regularly
- Monitor Streamlit Cloud app performance
- Set up alerts for data collection failures

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the project directory
   cd automated-esg-tracker
   
   # Activate virtual environment
   source venv/bin/activate
   ```

2. **Database Connection Issues**
   - Check your Supabase credentials
   - Ensure your IP is whitelisted (if required)
   - Verify database tables exist

3. **API Rate Limits**
   - Check your API usage
   - Implement proper delays between requests
   - Consider upgrading to paid tiers

4. **Streamlit Deployment Issues**
   - Check the deployment logs
   - Verify the main file path is correct
   - Ensure all dependencies are in requirements.txt

### Getting Help
- Check the GitHub Issues page
- Review Streamlit Cloud documentation
- Consult the README.md for detailed setup instructions

## 🎉 Success!

Once deployed, your ESG Data Tracker will be available at:
`https://your-app-name.streamlit.app`

Share this link in your portfolio, resume, and LinkedIn profile to showcase your fintech skills! 