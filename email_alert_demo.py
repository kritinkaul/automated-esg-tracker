#!/usr/bin/env python3
"""
Email Alert System Demo
Shows exactly how the email alert system works step by step
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time

def main():
    st.set_page_config(
        page_title="📧 Email Alert Demo",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 Email Alert System Demo")
    st.markdown("**See exactly how the email alert system works!**")
    
    # Step-by-step guide
    st.markdown("---")
    st.markdown("## 🚀 How It Works: Step-by-Step")
    
    with st.expander("📋 Step 1: User Signs Up for Alerts", expanded=True):
        st.markdown("""
        **User Journey:**
        1. User goes to the ESG Dashboard
        2. Clicks on "📧 Email Alerts" in the sidebar
        3. Fills out the signup form with:
           - Their email address
           - Alert types they want (ESG changes, carbon alerts, etc.)
           - Companies they want to monitor
           - Alert frequency (daily/weekly/monthly)
           - Change threshold (how big a change triggers an alert)
        4. Clicks "📧 Subscribe to Alerts"
        
        **What happens behind the scenes:**
        - System creates a user record in the database
        - Generates a verification token
        - Sends verification email to the user
        - Creates alert subscriptions based on their preferences
        """)
        
        # Demo form
        st.markdown("**Demo Signup Form:**")
        col1, col2 = st.columns(2)
        
        with col1:
            demo_email = st.text_input("📧 Email", value="demo@example.com", disabled=True)
            demo_alerts = st.multiselect(
                "Alert Types", 
                ["ESG Score Changes", "Carbon Alerts", "Weekly Summaries"],
                default=["ESG Score Changes", "Weekly Summaries"],
                disabled=True
            )
        
        with col2:
            demo_companies = st.multiselect(
                "Companies", 
                ["AAPL", "MSFT", "TSLA"],
                default=["AAPL", "TSLA"],
                disabled=True
            )
            demo_threshold = st.slider("Threshold (%)", 1.0, 20.0, 5.0, disabled=True)
        
        st.info("👆 This is what the signup form looks like!")
    
    with st.expander("📧 Step 2: Email Verification", expanded=False):
        st.markdown("""
        **Email Verification Process:**
        1. User receives a verification email like this:
        """)
        
        verification_email = """
        <div style="border: 2px solid #007bff; padding: 20px; border-radius: 10px; background: #f8f9fa;">
            <h3 style="color: #007bff;">🌱 Welcome to ESG Alerts</h3>
            <p>Thank you for signing up for ESG alerts!</p>
            <p>To complete your registration, please verify your email address.</p>
            <button style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
                ✅ Verify Email Address
            </button>
            <p><small>If you didn't sign up for ESG alerts, you can safely ignore this email.</small></p>
        </div>
        """
        st.markdown(verification_email, unsafe_allow_html=True)
        
        st.markdown("""
        2. User clicks the verification link
        3. System validates the token and activates their account
        4. User can now receive alerts!
        """)
    
    with st.expander("⚡ Step 3: System Monitors ESG Data", expanded=False):
        st.markdown("""
        **Continuous Monitoring:**
        - The system continuously monitors ESG data for all companies
        - When ESG scores change, it compares against user thresholds
        - If a change exceeds the threshold, an alert is triggered
        
        **Example Scenario:**
        """)
        
        # Demo data showing change
        monitoring_data = pd.DataFrame({
            'Company': ['AAPL', 'MSFT', 'TSLA', 'GOOGL'],
            'Previous ESG Score': [7.8, 8.1, 9.0, 7.9],
            'Current ESG Score': [8.0, 8.1, 9.2, 7.7],
            'Change %': [2.6, 0.0, 2.2, -2.5],
            'Alert Triggered': ['✅ Yes (>5%)', '❌ No', '❌ No', '❌ No']
        })
        
        st.dataframe(monitoring_data, use_container_width=True)
        
        st.markdown("""
        In this example:
        - **AAPL**: ESG score increased by 2.6% (alert triggered if user threshold ≤ 2.6%)
        - **MSFT**: No change (no alert)
        - **TSLA**: Small increase (no alert if threshold > 2.2%)
        - **GOOGL**: Decrease of 2.5% (alert triggered if user threshold ≤ 2.5%)
        """)
    
    with st.expander("📨 Step 4: Alerts Are Sent", expanded=False):
        st.markdown("""
        **When an alert is triggered:**
        1. System finds all users subscribed to that company/alert type
        2. Checks if the change exceeds their threshold
        3. Generates a personalized email
        4. Sends the email via SMTP
        5. Logs the sent alert in the database
        """)
        
        # Sample alert email
        st.markdown("**Sample Alert Email:**")
        alert_email = """
        <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background: #f8fff9;">
            <h3 style="color: #28a745;">🌱 ESG Alert: AAPL Score Increased</h3>
            <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p><strong>Apple Inc. (AAPL)</strong> ESG score has <strong style="color: green;">increased</strong></p>
                <div style="font-size: 24px; font-weight: bold; color: #28a745;">
                    7.8 → 8.0 (+2.6%)
                </div>
                <p><strong>Change:</strong> +2.6%</p>
            </div>
            <p>This change may indicate:</p>
            <ul>
                <li>New renewable energy initiatives</li>
                <li>Improved board diversity</li>
                <li>Enhanced supply chain transparency</li>
            </ul>
            <button style="background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 5px;">
                📊 View Full Report
            </button>
            <hr>
            <p><small>You're receiving this because you're subscribed to ESG updates for AAPL.</small></p>
        </div>
        """
        st.markdown(alert_email, unsafe_allow_html=True)
    
    with st.expander("📊 Step 5: Different Types of Alerts", expanded=False):
        st.markdown("**The system sends different types of alerts:**")
        
        alert_types_tab1, alert_types_tab2, alert_types_tab3 = st.tabs([
            "📈 ESG Score Changes", 
            "📅 Weekly Summaries", 
            "🌍 Carbon Alerts"
        ])
        
        with alert_types_tab1:
            st.markdown("**ESG Score Change Alerts:**")
            st.markdown("- Triggered when a company's ESG score changes significantly")
            st.markdown("- Users set their own threshold (e.g., 5% change)")
            st.markdown("- Sent immediately when change is detected")
            st.markdown("- Includes old score, new score, and percentage change")
        
        with alert_types_tab2:
            st.markdown("**Weekly Summary Alerts:**")
            st.markdown("- Sent every week to subscribed users")
            st.markdown("- Includes top ESG performers")
            st.markdown("- Lists companies to watch")
            st.markdown("- Highlights recent ESG news")
            
            # Sample weekly summary
            weekly_summary = """
            <div style="border: 1px solid #6c757d; padding: 15px; border-radius: 8px; background: #f8f9fa;">
                <h4>📊 Your Weekly ESG Summary</h4>
                <p><strong>🏆 Top Performers This Week:</strong></p>
                <ul>
                    <li>Apple (AAPL): 8.0 (+2.6%)</li>
                    <li>Microsoft (MSFT): 8.1 (no change)</li>
                    <li>Tesla (TSLA): 9.2 (+2.2%)</li>
                </ul>
                <p><strong>⚠️ Companies to Watch:</strong></p>
                <ul>
                    <li>Google (GOOGL): 7.7 (-2.5%)</li>
                </ul>
            </div>
            """
            st.markdown(weekly_summary, unsafe_allow_html=True)
        
        with alert_types_tab3:
            st.markdown("**Carbon Emissions Alerts:**")
            st.markdown("- Triggered when companies exceed carbon thresholds")
            st.markdown("- Helps track environmental performance")
            st.markdown("- Includes current emissions vs. threshold")
            st.markdown("- Sent when threshold is exceeded")
    
    # Live demo section
    st.markdown("---")
    st.markdown("## 🎮 Live Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📧 Try the Alert System")
        
        if st.button("🧪 Simulate ESG Score Change"):
            with st.spinner("Monitoring ESG scores..."):
                time.sleep(1)
            
            st.success("✅ ESG Score Change Detected!")
            st.info("📧 Alert would be sent to all subscribed users")
            
            # Show what would happen
            demo_alert = """
            <div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 10px; border-radius: 5px;">
                <strong>Alert Details:</strong><br>
                Company: AAPL<br>
                Old Score: 7.8<br>
                New Score: 8.0<br>
                Change: +2.6%<br>
                Recipients: 45 users
            </div>
            """
            st.markdown(demo_alert, unsafe_allow_html=True)
        
        if st.button("📅 Simulate Weekly Summary"):
            with st.spinner("Generating weekly summary..."):
                time.sleep(1)
            
            st.success("✅ Weekly Summary Generated!")
            st.info("📧 Summary would be sent to 298 weekly subscribers")
    
    with col2:
        st.markdown("### 📈 Alert Statistics")
        
        # Mock real-time stats
        stats_data = {
            'Metric': ['Total Users', 'Active Alerts', 'Emails Today', 'Success Rate'],
            'Value': ['1,247', '3,891', '156', '98.5%'],
            'Change': ['+12%', '+8%', '+23%', '+0.2%']
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Recent activity
        st.markdown("**Recent Alerts:**")
        recent_activity = pd.DataFrame({
            'Time': ['2 min ago', '5 min ago', '12 min ago'],
            'Alert': ['AAPL ESG +2.6%', 'TSLA Carbon Alert', 'Weekly Summary'],
            'Recipients': [45, 23, 298]
        })
        st.dataframe(recent_activity, use_container_width=True, hide_index=True)
    
    # Technical details
    st.markdown("---")
    st.markdown("## 🔧 Technical Details")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("### 🗄️ Database Structure")
        st.code("""
        Tables:
        - alert_users: User accounts & verification
        - alert_subscriptions: User preferences
        - sent_alerts: History of sent alerts
        
        Flow:
        1. User signs up → record in alert_users
        2. User sets preferences → alert_subscriptions
        3. Alert triggered → check subscriptions
        4. Email sent → log in sent_alerts
        """)
    
    with tech_col2:
        st.markdown("### 📧 Email Configuration")
        st.code("""
        Supported Providers:
        - Gmail (smtp.gmail.com:587)
        - Outlook (smtp-mail.outlook.com:587)
        - Yahoo (smtp.mail.yahoo.com:587)
        
        Requirements:
        - SMTP server & port
        - Email address & app password
        - 2-Factor Authentication enabled
        """)
    
    # Quick start guide
    st.markdown("---")
    st.markdown("## 🚀 Quick Start Guide")
    
    st.markdown("""
    **To set up email alerts on your ESG dashboard:**
    
    1. **Configure Email Settings:**
       ```bash
       streamlit run email_setup.py
       ```
    
    2. **Start the Dashboard:**
       ```bash
       streamlit run ultimate_dashboard.py
       ```
    
    3. **Navigate to Email Alerts:**
       - Click "📧 Email Alerts" in the sidebar
       - Go to "🔔 Sign Up" tab
       - Fill out your preferences
       - Verify your email
    
    4. **Start Receiving Alerts:**
       - System monitors ESG data automatically
       - Alerts sent when thresholds are exceeded
       - Manage subscriptions anytime
    """)
    
    # Benefits
    st.markdown("---")
    st.markdown("## 🌟 Benefits")
    
    benefits_col1, benefits_col2, benefits_col3 = st.columns(3)
    
    with benefits_col1:
        st.markdown("""
        ### 📊 **Stay Informed**
        - Real-time ESG updates
        - Never miss important changes
        - Customizable thresholds
        - Multiple alert types
        """)
    
    with benefits_col2:
        st.markdown("""
        ### ⚡ **Automated**
        - No manual checking needed
        - Continuous monitoring
        - Instant notifications
        - Reliable delivery
        """)
    
    with benefits_col3:
        st.markdown("""
        ### 🎯 **Personalized**
        - Choose your companies
        - Set your thresholds
        - Pick alert frequency
        - Manage preferences easily
        """)

if __name__ == "__main__":
    main() 