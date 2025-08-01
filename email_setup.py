#!/usr/bin/env python3
"""
Email Alert Setup Script
Helps users configure email alerts for the ESG dashboard
"""

import os
import streamlit as st
from pathlib import Path

def main():
    st.set_page_config(
        page_title="📧 Email Alert Setup",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 Email Alert Setup")
    st.markdown("Configure your email settings to receive ESG alerts")
    
    # Check if .env file exists
    env_file = Path(".env")
    env_exists = env_file.exists()
    
    if env_exists:
        st.success("✅ .env file found")
    else:
        st.warning("⚠️ .env file not found. Creating one...")
    
    st.markdown("---")
    
    # Email configuration form
    with st.form("email_config"):
        st.markdown("### 🔧 Email Configuration")
        
        st.markdown("""
        **To send email alerts, you need to configure SMTP settings.**
        
        **Popular options:**
        - **Gmail**: smtp.gmail.com:587 (requires App Password)
        - **Outlook**: smtp-mail.outlook.com:587
        - **Yahoo**: smtp.mail.yahoo.com:587
        """)
        
        smtp_server = st.text_input(
            "SMTP Server",
            value="smtp.gmail.com",
            help="Your email provider's SMTP server"
        )
        
        smtp_port = st.number_input(
            "SMTP Port",
            value=587,
            min_value=1,
            max_value=65535,
            help="Usually 587 for TLS or 465 for SSL"
        )
        
        email_address = st.text_input(
            "Email Address",
            placeholder="your.email@gmail.com",
            help="The email address that will send alerts"
        )
        
        email_password = st.text_input(
            "Email Password/App Password",
            type="password",
            help="For Gmail, use an App Password instead of your regular password"
        )
        
        from_name = st.text_input(
            "From Name",
            value="ESG Data Tracker",
            help="The name that will appear in email alerts"
        )
        
        submitted = st.form_submit_button("💾 Save Configuration")
        
        if submitted:
            if email_address and email_password:
                # Create or update .env file
                env_content = f"""# Email Alert Configuration
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
EMAIL_ADDRESS={email_address}
EMAIL_PASSWORD={email_password}
FROM_NAME={from_name}

# Other API Keys (keep existing ones)
"""
                
                # Read existing .env content if it exists
                if env_exists:
                    with open(".env", "r") as f:
                        existing_content = f.read()
                    
                    # Extract non-email settings
                    lines = existing_content.split('\n')
                    other_settings = []
                    for line in lines:
                        if not any(keyword in line for keyword in ['SMTP_', 'EMAIL_', 'FROM_']):
                            other_settings.append(line)
                    
                    env_content += '\n'.join(other_settings)
                
                # Write to .env file
                with open(".env", "w") as f:
                    f.write(env_content)
                
                st.success("✅ Email configuration saved!")
                st.info("📧 You can now receive email alerts from the ESG dashboard.")
                
            else:
                st.error("❌ Please fill in all required fields.")
    
    st.markdown("---")
    
    # Test email functionality
    st.markdown("### 🧪 Test Email Configuration")
    
    if st.button("📧 Send Test Email"):
        if email_address and email_password:
            try:
                from src.email_alert_system import EmailSender
                
                email_sender = EmailSender()
                test_html = """
                <html>
                <body>
                    <h2>🧪 Test Email from ESG Data Tracker</h2>
                    <p>This is a test email to verify your email configuration is working correctly.</p>
                    <p>If you received this email, your email alerts are properly configured!</p>
                </body>
                </html>
                """
                
                success = email_sender.send_email(
                    to_email=email_address,
                    subject="🧪 ESG Alert System Test",
                    html_content=test_html
                )
                
                if success:
                    st.success("✅ Test email sent successfully!")
                else:
                    st.error("❌ Failed to send test email. Check your configuration.")
                    
            except Exception as e:
                st.error(f"❌ Error sending test email: {e}")
        else:
            st.error("❌ Please configure email settings first.")
    
    st.markdown("---")
    
    # Instructions for different email providers
    st.markdown("### 📚 Setup Instructions")
    
    with st.expander("📧 Gmail Setup"):
        st.markdown("""
        **Gmail Setup Instructions:**
        
        1. **Enable 2-Factor Authentication** on your Google account
        2. **Generate an App Password:**
           - Go to Google Account settings
           - Security → 2-Step Verification → App passwords
           - Generate a new app password for "Mail"
        3. **Use these settings:**
           - SMTP Server: `smtp.gmail.com`
           - SMTP Port: `587`
           - Email: your Gmail address
           - Password: the App Password (not your regular password)
        """)
    
    with st.expander("📧 Outlook Setup"):
        st.markdown("""
        **Outlook Setup Instructions:**
        
        1. **Enable 2-Factor Authentication** on your Microsoft account
        2. **Generate an App Password:**
           - Go to Microsoft Account settings
           - Security → Advanced security options → App passwords
           - Generate a new app password
        3. **Use these settings:**
           - SMTP Server: `smtp-mail.outlook.com`
           - SMTP Port: `587`
           - Email: your Outlook address
           - Password: the App Password
        """)
    
    with st.expander("📧 Yahoo Setup"):
        st.markdown("""
        **Yahoo Setup Instructions:**
        
        1. **Enable 2-Factor Authentication** on your Yahoo account
        2. **Generate an App Password:**
           - Go to Yahoo Account Security
           - App passwords → Generate app password
        3. **Use these settings:**
           - SMTP Server: `smtp.mail.yahoo.com`
           - SMTP Port: `587`
           - Email: your Yahoo address
           - Password: the App Password
        """)
    
    st.markdown("---")
    
    # Troubleshooting
    st.markdown("### 🔧 Troubleshooting")
    
    with st.expander("❓ Common Issues"):
        st.markdown("""
        **Common Email Issues:**
        
        **"Authentication failed"**
        - Make sure you're using an App Password, not your regular password
        - Verify 2-Factor Authentication is enabled
        
        **"Connection refused"**
        - Check your SMTP server and port
        - Try different ports (587, 465, 25)
        
        **"SSL/TLS error"**
        - Try port 587 with STARTTLS
        - Or try port 465 with SSL
        
        **Gmail specific:**
        - Make sure "Less secure app access" is enabled (if not using App Password)
        - Or use App Password with 2FA enabled
        """)

if __name__ == "__main__":
    main() 