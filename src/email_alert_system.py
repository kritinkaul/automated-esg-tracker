"""
Email Alert System for ESG Data Tracker
Handles user signup, email alerts, and notification management
"""

import os
import smtplib
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import sqlite3
from dataclasses import dataclass
from enum import Enum
import hashlib
import secrets
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertType(Enum):
    """Types of alerts that can be sent."""
    ESG_SCORE_CHANGE = "esg_score_change"
    CARBON_EMISSIONS_ALERT = "carbon_emissions_alert"
    NEWS_ALERT = "news_alert"
    STOCK_PRICE_ALERT = "stock_price_alert"
    WEEKLY_SUMMARY = "weekly_summary"
    MONTHLY_REPORT = "monthly_report"


@dataclass
class AlertConfig:
    """Configuration for email alerts."""
    email: str
    alert_types: List[AlertType]
    companies: List[str]
    frequency: str  # "daily", "weekly", "monthly"
    threshold: float = 0.05  # 5% change threshold
    is_active: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class EmailTemplate:
    """Email template manager."""
    
    @staticmethod
    def get_esg_score_alert_template(company: str, old_score: float, new_score: float, change_percent: float) -> str:
        """Generate ESG score alert email template."""
        direction = "increased" if new_score > old_score else "decreased"
        color = "#28a745" if new_score > old_score else "#dc3545"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .alert-box {{ background: #f8f9fa; border-left: 4px solid {color}; padding: 15px; margin: 20px 0; }}
                .score-change {{ font-size: 24px; font-weight: bold; color: {color}; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
                .button {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
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
                    <p><strong>Change:</strong> {change_percent:+.1f}%</p>
                </div>
                <p>This change may indicate:</p>
                <ul>
                    <li>Environmental policy updates</li>
                    <li>Social responsibility initiatives</li>
                    <li>Governance structure changes</li>
                    <li>Regulatory compliance updates</li>
                </ul>
                <p style="text-align: center;">
                    <a href="#" class="button">View Full Report</a>
                </p>
            </div>
            <div class="footer">
                <p>You're receiving this alert because you're subscribed to ESG updates for {company}.</p>
                <p><a href="#">Unsubscribe</a> | <a href="#">Manage Alerts</a></p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_weekly_summary_template(user_email: str, summary_data: Dict[str, Any]) -> str:
        """Generate weekly summary email template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .summary-box {{ background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; }}
                .metric {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
                .button {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Weekly ESG Summary</h1>
                <p>Your ESG tracking summary for the week</p>
            </div>
            <div class="content">
                <h2>Hello {user_email.split('@')[0]},</h2>
                <p>Here's your weekly ESG summary:</p>
                
                <div class="summary-box">
                    <h3>📈 Top Performers</h3>
                    {''.join([f'<div class="metric"><span>{company}</span><span>{score:.2f}</span></div>' for company, score in summary_data.get('top_performers', [])])}
                </div>
                
                <div class="summary-box">
                    <h3>📉 Companies to Watch</h3>
                    {''.join([f'<div class="metric"><span>{company}</span><span>{score:.2f}</span></div>' for company, score in summary_data.get('companies_to_watch', [])])}
                </div>
                
                <div class="summary-box">
                    <h3>📰 Recent News Highlights</h3>
                    {''.join([f'<p>• {news}</p>' for news in summary_data.get('news_highlights', [])])}
                </div>
                
                <p style="text-align: center;">
                    <a href="#" class="button">View Full Dashboard</a>
                </p>
            </div>
            <div class="footer">
                <p>You're receiving this because you're subscribed to weekly ESG summaries.</p>
                <p><a href="#">Unsubscribe</a> | <a href="#">Manage Alerts</a></p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_carbon_alert_template(company: str, emissions: float, threshold: float) -> str:
        """Generate carbon emissions alert template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .alert-box {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌍 Carbon Emissions Alert</h1>
                <p>High Carbon Emissions Detected</p>
            </div>
            <div class="content">
                <h2>Carbon Alert for {company}</h2>
                <div class="alert-box">
                    <p><strong>Current Emissions:</strong> {emissions:.2f} tons CO2</p>
                    <p><strong>Threshold:</strong> {threshold:.2f} tons CO2</p>
                    <p>This company's carbon emissions have exceeded the alert threshold.</p>
                </div>
                <p>Consider reviewing their environmental policies and sustainability initiatives.</p>
            </div>
            <div class="footer">
                <p>You're receiving this alert because you're monitoring {company}.</p>
                <p><a href="#">Unsubscribe</a> | <a href="#">Manage Alerts</a></p>
            </div>
        </body>
        </html>
        """


class EmailSender:
    """Handles email sending functionality."""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.from_name = os.getenv('FROM_NAME', 'ESG Data Tracker')
        
        if not all([self.email_address, self.email_password]):
            logger.warning("Email credentials not configured. Alerts will be logged only.")
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send an email with HTML content."""
        if not self.email_address or not self.email_password:
            logger.info(f"Email alert (not sent): {subject} to {to_email}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.email_address}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add text content if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully: {subject} to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False


class AlertManager:
    """Manages alert subscriptions and sending."""
    
    def __init__(self):
        self.db_path = "data/email_alerts.db"
        self.email_sender = EmailSender()
        self._init_database()
    
    def _init_database(self):
        """Initialize the alerts database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                verification_token TEXT,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create alert subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                companies TEXT,  -- JSON array of company tickers
                frequency TEXT DEFAULT 'daily',
                threshold REAL DEFAULT 0.05,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES alert_users (id)
            )
        ''')
        
        # Create sent alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                company TEXT,
                subject TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES alert_users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def signup_user(self, email: str) -> Dict[str, Any]:
        """Sign up a new user for email alerts."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM alert_users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return {"success": False, "message": "Email already registered"}
            
            # Generate verification token
            verification_token = secrets.token_urlsafe(32)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO alert_users (email, verification_token, is_verified)
                VALUES (?, ?, FALSE)
            ''', (email, verification_token))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Send verification email
            self._send_verification_email(email, verification_token)
            
            return {
                "success": True, 
                "message": "Signup successful! Please check your email to verify your account.",
                "user_id": user_id
            }
            
        except Exception as e:
            logger.error(f"Error signing up user {email}: {e}")
            return {"success": False, "message": "Signup failed. Please try again."}
    
    def verify_user(self, token: str) -> Dict[str, Any]:
        """Verify a user's email address."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE alert_users 
                SET is_verified = TRUE, verification_token = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE verification_token = ?
            ''', (token,))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return {"success": True, "message": "Email verified successfully!"}
            else:
                conn.close()
                return {"success": False, "message": "Invalid verification token"}
                
        except Exception as e:
            logger.error(f"Error verifying user: {e}")
            return {"success": False, "message": "Verification failed"}
    
    def add_alert_subscription(self, email: str, alert_type: str, companies: List[str] = None, 
                              frequency: str = "daily", threshold: float = 0.05) -> Dict[str, Any]:
        """Add an alert subscription for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user ID
            cursor.execute('SELECT id FROM alert_users WHERE email = ? AND is_verified = TRUE', (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return {"success": False, "message": "User not found or not verified"}
            
            user_id = user[0]
            companies_json = json.dumps(companies or [])
            
            # Insert subscription
            cursor.execute('''
                INSERT INTO alert_subscriptions (user_id, alert_type, companies, frequency, threshold)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, alert_type, companies_json, frequency, threshold))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "Alert subscription added successfully"}
            
        except Exception as e:
            logger.error(f"Error adding alert subscription: {e}")
            return {"success": False, "message": "Failed to add subscription"}
    
    def get_user_subscriptions(self, email: str) -> List[Dict[str, Any]]:
        """Get all subscriptions for a user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.id, s.alert_type, s.companies, s.frequency, s.threshold, s.is_active
                FROM alert_subscriptions s
                JOIN alert_users u ON s.user_id = u.id
                WHERE u.email = ? AND u.is_verified = TRUE
            ''', (email,))
            
            subscriptions = []
            for row in cursor.fetchall():
                subscriptions.append({
                    "id": row[0],
                    "alert_type": row[1],
                    "companies": json.loads(row[2]) if row[2] else [],
                    "frequency": row[3],
                    "threshold": row[4],
                    "is_active": bool(row[5])
                })
            
            conn.close()
            return subscriptions
            
        except Exception as e:
            logger.error(f"Error getting user subscriptions: {e}")
            return []
    
    def send_esg_score_alert(self, company: str, old_score: float, new_score: float, 
                            change_percent: float) -> int:
        """Send ESG score change alerts to subscribed users."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get users subscribed to ESG score alerts
            cursor.execute('''
                SELECT DISTINCT u.email, s.threshold
                FROM alert_users u
                JOIN alert_subscriptions s ON u.id = s.user_id
                WHERE s.alert_type = 'esg_score_change' 
                AND s.is_active = TRUE 
                AND u.is_verified = TRUE
                AND (s.companies IS NULL OR s.companies = '[]' OR s.companies LIKE ?)
            ''', (f'%"{company}"%',))
            
            sent_count = 0
            for row in cursor.fetchall():
                email, threshold = row
                
                # Check if change exceeds threshold
                if abs(change_percent) >= (threshold * 100):
                    subject = f"ESG Alert: {company} Score Changed by {change_percent:+.1f}%"
                    html_content = EmailTemplate.get_esg_score_alert_template(
                        company, old_score, new_score, change_percent
                    )
                    
                    if self.email_sender.send_email(email, subject, html_content):
                        sent_count += 1
                        
                        # Log sent alert
                        cursor.execute('''
                            INSERT INTO sent_alerts (user_id, alert_type, company, subject)
                            SELECT u.id, 'esg_score_change', ?, ?
                            FROM alert_users u WHERE u.email = ?
                        ''', (company, subject, email))
            
            conn.commit()
            conn.close()
            return sent_count
            
        except Exception as e:
            logger.error(f"Error sending ESG score alerts: {e}")
            return 0
    
    def send_weekly_summary(self) -> int:
        """Send weekly summary to all users with weekly subscriptions."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT u.email
                FROM alert_users u
                JOIN alert_subscriptions s ON u.id = s.user_id
                WHERE s.frequency = 'weekly' AND s.is_active = TRUE AND u.is_verified = TRUE
            ''')
            
            sent_count = 0
            for row in cursor.fetchall():
                email = row[0]
                
                # Generate summary data (this would come from your ESG data)
                summary_data = {
                    "top_performers": [("Apple", 8.5), ("Microsoft", 8.2), ("Tesla", 7.9)],
                    "companies_to_watch": [("Exxon", 4.2), ("Chevron", 4.5)],
                    "news_highlights": [
                        "Apple announces new renewable energy initiatives",
                        "Microsoft commits to carbon neutrality by 2030",
                        "Tesla expands solar panel production"
                    ]
                }
                
                subject = "📊 Your Weekly ESG Summary"
                html_content = EmailTemplate.get_weekly_summary_template(email, summary_data)
                
                if self.email_sender.send_email(email, subject, html_content):
                    sent_count += 1
                    
                    # Log sent alert
                    cursor.execute('''
                        INSERT INTO sent_alerts (user_id, alert_type, subject)
                        SELECT u.id, 'weekly_summary', ?
                        FROM alert_users u WHERE u.email = ?
                    ''', (subject, email))
            
            conn.commit()
            conn.close()
            return sent_count
            
        except Exception as e:
            logger.error(f"Error sending weekly summaries: {e}")
            return 0
    
    def _send_verification_email(self, email: str, token: str):
        """Send verification email to new user."""
        subject = "Verify Your ESG Alert Subscription"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
                .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌱 Welcome to ESG Alerts</h1>
                <p>Verify your email to start receiving alerts</p>
            </div>
            <div class="content">
                <h2>Welcome to ESG Data Tracker!</h2>
                <p>Thank you for signing up for ESG alerts. To complete your registration, please verify your email address.</p>
                <p style="text-align: center;">
                    <a href="#" class="button">Verify Email Address</a>
                </p>
                <p>Or copy and paste this link in your browser:</p>
                <p style="word-break: break-all; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                    http://localhost:8501/verify?token={token}
                </p>
            </div>
            <div class="footer">
                <p>If you didn't sign up for ESG alerts, you can safely ignore this email.</p>
            </div>
        </body>
        </html>
        """
        
        self.email_sender.send_email(email, subject, html_content)


# Global alert manager instance
alert_manager = AlertManager() 