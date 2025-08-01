"""
Email Alert Dashboard Component
Streamlit component for email alert signup and management
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from src.email_alert_system import AlertManager, AlertType

# Initialize alert manager
alert_manager = AlertManager()

def render_email_alert_signup():
    """Render the email alert signup section."""
    st.markdown("---")
    st.markdown("### 📧 Email Alert Signup")
    
    with st.expander("🔔 Get Email Alerts", expanded=False):
        st.markdown("""
        Stay informed about ESG changes with email alerts:
        - **ESG Score Changes**: Get notified when companies' ESG scores change significantly
        - **Carbon Emissions Alerts**: Monitor companies exceeding carbon thresholds
        - **Weekly Summaries**: Receive weekly ESG performance summaries
        - **News Alerts**: Get notified about important ESG-related news
        """)
        
        # Email signup form
        with st.form("email_signup_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            
            st.markdown("**Alert Types:**")
            alert_types = st.multiselect(
                "Select alert types:",
                options=[
                    ("ESG Score Changes", "esg_score_change"),
                    ("Carbon Emissions Alerts", "carbon_emissions_alert"),
                    ("News Alerts", "news_alert"),
                    ("Weekly Summaries", "weekly_summary"),
                    ("Monthly Reports", "monthly_report")
                ],
                format_func=lambda x: x[0],
                default=["esg_score_change", "weekly_summary"]
            )
            
            st.markdown("**Companies to Monitor:**")
            companies = st.multiselect(
                "Select companies (leave empty for all):",
                options=["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA", "NFLX"],
                default=["AAPL", "MSFT", "TSLA"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                frequency = st.selectbox(
                    "Alert Frequency:",
                    options=["daily", "weekly", "monthly"],
                    index=1
                )
            
            with col2:
                threshold = st.slider(
                    "Change Threshold (%):",
                    min_value=1.0,
                    max_value=20.0,
                    value=5.0,
                    step=0.5
                )
            
            submitted = st.form_submit_button("📧 Subscribe to Alerts")
            
            if submitted:
                if email and "@" in email:
                    # Sign up user
                    signup_result = alert_manager.signup_user(email)
                    
                    if signup_result["success"]:
                        st.success("✅ " + signup_result["message"])
                        
                        # Add alert subscriptions
                        for alert_type in alert_types:
                            alert_manager.add_alert_subscription(
                                email=email,
                                alert_type=alert_type[1],
                                companies=companies,
                                frequency=frequency,
                                threshold=threshold/100
                            )
                        
                        st.info("📧 Please check your email to verify your account and start receiving alerts!")
                    else:
                        st.error("❌ " + signup_result["message"])
                else:
                    st.error("❌ Please enter a valid email address")

def render_alert_management():
    """Render the alert management section."""
    st.markdown("### ⚙️ Manage Your Alerts")
    
    with st.expander("🔧 Alert Settings", expanded=False):
        email = st.text_input("📧 Enter your email to manage alerts:", placeholder="your.email@example.com")
        
        if email and "@" in email:
            # Get user subscriptions
            subscriptions = alert_manager.get_user_subscriptions(email)
            
            if subscriptions:
                st.markdown("**Your Current Subscriptions:**")
                
                for i, sub in enumerate(subscriptions):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            st.markdown(f"**{sub['alert_type'].replace('_', ' ').title()}**")
                            st.markdown(f"Companies: {', '.join(sub['companies']) if sub['companies'] else 'All'}")
                        
                        with col2:
                            st.markdown(f"Frequency: {sub['frequency']}")
                            st.markdown(f"Threshold: {sub['threshold']*100:.1f}%")
                        
                        with col3:
                            if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                                # Remove subscription logic would go here
                                st.success("Subscription removed!")
                                st.rerun()
                
                st.markdown("---")
                st.markdown("**Add New Alert:**")
                
                with st.form("add_alert_form"):
                    new_alert_type = st.selectbox(
                        "Alert Type:",
                        options=[
                            ("ESG Score Changes", "esg_score_change"),
                            ("Carbon Emissions Alerts", "carbon_emissions_alert"),
                            ("News Alerts", "news_alert"),
                            ("Weekly Summaries", "weekly_summary"),
                            ("Monthly Reports", "monthly_report")
                        ],
                        format_func=lambda x: x[0]
                    )
                    
                    new_companies = st.multiselect(
                        "Companies:",
                        options=["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA", "NFLX"],
                        default=["AAPL"]
                    )
                    
                    new_frequency = st.selectbox("Frequency:", ["daily", "weekly", "monthly"])
                    new_threshold = st.slider("Threshold (%):", 1.0, 20.0, 5.0, 0.5)
                    
                    if st.form_submit_button("➕ Add Alert"):
                        result = alert_manager.add_alert_subscription(
                            email=email,
                            alert_type=new_alert_type[1],
                            companies=new_companies,
                            frequency=new_frequency,
                            threshold=new_threshold/100
                        )
                        
                        if result["success"]:
                            st.success("✅ Alert added successfully!")
                            st.rerun()
                        else:
                            st.error("❌ " + result["message"])
            
            else:
                st.info("📧 No subscriptions found. Please sign up for alerts first.")

def render_alert_preview():
    """Render a preview of what alerts look like."""
    st.markdown("### 📋 Alert Preview")
    
    with st.expander("👀 See Sample Alerts", expanded=False):
        tab1, tab2, tab3 = st.tabs(["ESG Score Alert", "Weekly Summary", "Carbon Alert"])
        
        with tab1:
            st.markdown("**Sample ESG Score Change Alert:**")
            sample_html = """
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9;">
                <h3>🌱 ESG Alert: AAPL Score Changed by +2.3%</h3>
                <p><strong>Apple Inc.</strong> ESG score has increased from 7.8 to 8.0 (+2.3%)</p>
                <p>This change may indicate:</p>
                <ul>
                    <li>New renewable energy initiatives</li>
                    <li>Improved board diversity</li>
                    <li>Enhanced supply chain transparency</li>
                </ul>
            </div>
            """
            st.markdown(sample_html, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("**Sample Weekly Summary:**")
            sample_summary = """
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9;">
                <h3>📊 Your Weekly ESG Summary</h3>
                <p><strong>Top Performers:</strong></p>
                <ul>
                    <li>Apple (AAPL): 8.0 (+2.3%)</li>
                    <li>Microsoft (MSFT): 7.9 (+1.5%)</li>
                    <li>Tesla (TSLA): 7.7 (+0.8%)</li>
                </ul>
                <p><strong>Companies to Watch:</strong></p>
                <ul>
                    <li>Exxon (XOM): 4.2 (-1.2%)</li>
                    <li>Chevron (CVX): 4.5 (-0.8%)</li>
                </ul>
            </div>
            """
            st.markdown(sample_summary, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("**Sample Carbon Emissions Alert:**")
            sample_carbon = """
            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9;">
                <h3>🌍 Carbon Emissions Alert: XOM</h3>
                <p><strong>Exxon Mobil</strong> carbon emissions have exceeded the alert threshold:</p>
                <ul>
                    <li>Current Emissions: 125.3 tons CO2</li>
                    <li>Threshold: 100.0 tons CO2</li>
                    <li>Status: ⚠️ Above Threshold</li>
                </ul>
            </div>
            """
            st.markdown(sample_carbon, unsafe_allow_html=True)

def render_alert_statistics():
    """Render alert statistics and analytics."""
    st.markdown("### 📊 Alert Statistics")
    
    with st.expander("📈 Alert Analytics", expanded=False):
        # Mock statistics - in a real implementation, these would come from the database
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Subscribers", "1,247", "+12%")
        
        with col2:
            st.metric("Active Alerts", "3,891", "+8%")
        
        with col3:
            st.metric("Emails Sent Today", "156", "+23%")
        
        with col4:
            st.metric("Avg. Open Rate", "68%", "+5%")
        
        # Alert type distribution
        st.markdown("**Alert Type Distribution:**")
        alert_data = pd.DataFrame({
            'Alert Type': ['ESG Score Changes', 'Carbon Alerts', 'News Alerts', 'Weekly Summaries', 'Monthly Reports'],
            'Subscribers': [456, 234, 189, 298, 70]
        })
        
        st.bar_chart(alert_data.set_index('Alert Type'))
        
        # Recent activity
        st.markdown("**Recent Alert Activity:**")
        recent_alerts = pd.DataFrame({
            'Time': ['2 min ago', '5 min ago', '12 min ago', '1 hour ago', '2 hours ago'],
            'Alert': ['AAPL ESG score +2.3%', 'TSLA carbon alert', 'MSFT news alert', 'Weekly summary sent', 'XOM emissions alert'],
            'Recipients': [45, 23, 67, 298, 12]
        })
        
        st.dataframe(recent_alerts, use_container_width=True)

def main():
    """Main function to run the email alert dashboard."""
    st.set_page_config(
        page_title="📧 Email Alert System",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 ESG Email Alert System")
    st.markdown("Manage your ESG email alerts and notifications")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔔 Sign Up", 
        "⚙️ Manage Alerts", 
        "👀 Preview", 
        "📊 Statistics"
    ])
    
    with tab1:
        render_email_alert_signup()
    
    with tab2:
        render_alert_management()
    
    with tab3:
        render_alert_preview()
    
    with tab4:
        render_alert_statistics()

if __name__ == "__main__":
    main() 