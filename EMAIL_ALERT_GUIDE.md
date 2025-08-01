# 📧 ESG Email Alert System Guide

## 🌟 Overview

The ESG Email Alert System provides automated email notifications for important ESG-related changes and events. Users can sign up for alerts through the dashboard and receive personalized notifications about ESG score changes, carbon emissions, news alerts, and periodic summaries.

## 🚀 Features

### ✅ Core Features
- **Email Alert Signup**: Users can subscribe to different types of alerts
- **Alert Types**: ESG score changes, carbon emissions, news alerts, weekly/monthly summaries
- **Company Filtering**: Subscribe to alerts for specific companies or all companies
- **Customizable Thresholds**: Set percentage change thresholds for alerts
- **Frequency Control**: Daily, weekly, or monthly alert frequencies
- **Email Verification**: Secure email verification system
- **Alert Management**: Users can manage and modify their subscriptions

### 📧 Alert Types
1. **ESG Score Changes**: Notifications when company ESG scores change significantly
2. **Carbon Emissions Alerts**: Alerts when companies exceed carbon thresholds
3. **News Alerts**: Important ESG-related news notifications
4. **Weekly Summaries**: Comprehensive weekly ESG performance summaries
5. **Monthly Reports**: Detailed monthly ESG analysis reports

## 🛠️ Installation & Setup

### 1. Prerequisites
```bash
# Ensure you have the required packages
pip install streamlit pandas plotly requests python-dotenv
```

### 2. Email Configuration
Run the email setup script to configure SMTP settings:

```bash
streamlit run email_setup.py
```

Or manually add to your `.env` file:
```bash
# Email Alert Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
FROM_NAME=ESG Data Tracker
```

### 3. Database Setup
The email alert system uses SQLite for storing user subscriptions and alert history:

```bash
# The database will be created automatically in data/email_alerts.db
# No manual setup required
```

## 📊 Dashboard Integration

### Main Dashboard
The email alert system is integrated into the main ESG dashboard:

1. **Navigation**: Select "📧 Email Alerts" from the sidebar
2. **Signup Tab**: Subscribe to email alerts
3. **Management Tab**: Manage existing subscriptions
4. **Preview Tab**: See sample alert emails
5. **Statistics Tab**: View alert analytics

### Alert Triggers
Alerts are automatically triggered when:
- ESG scores change by more than the threshold percentage
- Carbon emissions exceed configured limits
- New ESG-related news is detected
- Weekly/monthly summary schedules are reached

## 🔧 Configuration

### Email Provider Setup

#### Gmail
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use settings:
   - SMTP Server: `smtp.gmail.com`
   - SMTP Port: `587`
   - Password: App Password (not regular password)

#### Outlook
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Microsoft Account → Security → Advanced security → App passwords
3. Use settings:
   - SMTP Server: `smtp-mail.outlook.com`
   - SMTP Port: `587`

#### Yahoo
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Yahoo Account Security → App passwords
3. Use settings:
   - SMTP Server: `smtp.mail.yahoo.com`
   - SMTP Port: `587`

## 📧 Email Templates

### ESG Score Alert Template
```html
<div class="header">
    <h1>🌱 ESG Alert</h1>
    <p>Important ESG Score Change Detected</p>
</div>
<div class="content">
    <h2>ESG Score Alert for {company}</h2>
    <div class="alert-box">
        <p>The ESG score for <strong>{company}</strong> has {direction}.</p>
        <div class="score-change">
            {old_score:.2f} → {new_score:.2f} ({change_percent:+.1f}%)
        </div>
    </div>
</div>
```

### Weekly Summary Template
```html
<div class="header">
    <h1>📊 Weekly ESG Summary</h1>
    <p>Your ESG tracking summary for the week</p>
</div>
<div class="content">
    <h2>Hello {user_email},</h2>
    <div class="summary-box">
        <h3>📈 Top Performers</h3>
        {top_performers_list}
    </div>
    <div class="summary-box">
        <h3>📉 Companies to Watch</h3>
        {companies_to_watch_list}
    </div>
</div>
```

## 🗄️ Database Schema

### Alert Users Table
```sql
CREATE TABLE alert_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    verification_token TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Alert Subscriptions Table
```sql
CREATE TABLE alert_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,
    companies TEXT,  -- JSON array of company tickers
    frequency TEXT DEFAULT 'daily',
    threshold REAL DEFAULT 0.05,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES alert_users (id)
);
```

### Sent Alerts Table
```sql
CREATE TABLE sent_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    alert_type TEXT NOT NULL,
    company TEXT,
    subject TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES alert_users (id)
);
```

## 🔄 API Integration

### Alert Manager Class
```python
from src.email_alert_system import AlertManager

# Initialize alert manager
alert_manager = AlertManager()

# Sign up user
result = alert_manager.signup_user("user@example.com")

# Add alert subscription
alert_manager.add_alert_subscription(
    email="user@example.com",
    alert_type="esg_score_change",
    companies=["AAPL", "MSFT"],
    frequency="daily",
    threshold=0.05
)

# Send ESG score alert
alert_manager.send_esg_score_alert(
    company="AAPL",
    old_score=7.8,
    new_score=8.0,
    change_percent=2.3
)
```

## 🧪 Testing

### Test Email Configuration
```bash
# Run the email setup script
streamlit run email_setup.py

# Click "Send Test Email" to verify configuration
```

### Test Alert System
```python
# Test alert sending
from src.email_alert_system import alert_manager

# Send test alert
alert_manager.send_esg_score_alert(
    company="TEST",
    old_score=7.5,
    new_score=8.0,
    change_percent=6.7
)
```

## 📈 Monitoring & Analytics

### Alert Statistics
- Total subscribers
- Active alerts
- Emails sent today
- Average open rate
- Alert type distribution

### Recent Activity
- Recent alert activity
- Alert performance metrics
- User engagement statistics

## 🔒 Security Features

### Email Verification
- Secure token-based email verification
- Automatic token expiration
- Protection against unauthorized signups

### Data Protection
- Encrypted password storage
- Secure SMTP connections
- User data privacy compliance

## 🚨 Troubleshooting

### Common Issues

#### "Authentication failed"
- Verify you're using an App Password, not regular password
- Check that 2-Factor Authentication is enabled
- Ensure SMTP server and port are correct

#### "Connection refused"
- Check firewall settings
- Verify SMTP server and port
- Try different ports (587, 465, 25)

#### "SSL/TLS error"
- Try port 587 with STARTTLS
- Or try port 465 with SSL
- Check email provider's security settings

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed SMTP communication
```

## 📝 Usage Examples

### Basic Alert Signup
1. Navigate to "📧 Email Alerts" in the dashboard
2. Click "🔔 Sign Up" tab
3. Enter your email address
4. Select alert types (ESG Score Changes, Weekly Summaries)
5. Choose companies to monitor
6. Set frequency and threshold
7. Click "📧 Subscribe to Alerts"
8. Verify your email address

### Managing Alerts
1. Go to "⚙️ Manage Alerts" tab
2. Enter your email address
3. View current subscriptions
4. Add new alerts or remove existing ones
5. Modify thresholds and frequencies

### Alert Preview
1. Click "👀 Preview" tab
2. View sample alert emails
3. See different alert types and formats
4. Understand what alerts look like

## 🔮 Future Enhancements

### Planned Features
- **SMS Alerts**: Text message notifications
- **Push Notifications**: Browser push notifications
- **Advanced Filtering**: More granular alert criteria
- **Alert Scheduling**: Custom alert schedules
- **Integration APIs**: Connect with external systems
- **Analytics Dashboard**: Detailed alert analytics
- **A/B Testing**: Test different alert formats
- **Multi-language Support**: Internationalization

### Technical Improvements
- **Real-time Alerts**: WebSocket-based instant notifications
- **Machine Learning**: Smart alert prioritization
- **Advanced Templates**: Dynamic email templates
- **Performance Optimization**: Faster alert processing
- **Scalability**: Handle large user bases

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review email provider setup instructions
- Test email configuration with the setup script
- Check logs for detailed error messages

### Contact Information
- **Documentation**: See this guide and inline code comments
- **Issues**: Check the project repository for known issues
- **Community**: Join the project community for support

---

**🎉 Congratulations!** You now have a fully functional email alert system for your ESG dashboard. Users can sign up for alerts, receive notifications about important ESG changes, and manage their subscriptions through an intuitive interface. 