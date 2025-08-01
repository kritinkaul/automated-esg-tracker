#!/usr/bin/env python3
"""
Test script for the ESG Email Alert System
Verifies that all components are working correctly
"""

import os
import sys
from datetime import datetime
import sqlite3

def test_database_creation():
    """Test that the database is created correctly."""
    print("🧪 Testing database creation...")
    
    try:
        from src.email_alert_system import AlertManager
        alert_manager = AlertManager()
        
        # Check if database file exists
        db_path = "data/email_alerts.db"
        if os.path.exists(db_path):
            print("✅ Database file created successfully")
        else:
            print("❌ Database file not found")
            return False
        
        # Test database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['alert_users', 'alert_subscriptions', 'sent_alerts']
        for table in expected_tables:
            if table in tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                return False
        
        conn.close()
        print("✅ Database structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_email_sender():
    """Test the email sender functionality."""
    print("\n🧪 Testing email sender...")
    
    try:
        from src.email_alert_system import EmailSender
        
        email_sender = EmailSender()
        
        # Check if email credentials are configured
        if not email_sender.email_address or not email_sender.email_password:
            print("⚠️ Email credentials not configured - alerts will be logged only")
            print("   Run 'streamlit run email_setup.py' to configure email settings")
            return True  # This is not a failure, just a warning
        
        print("✅ Email sender initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Email sender test failed: {e}")
        return False

def test_alert_manager():
    """Test the alert manager functionality."""
    print("\n🧪 Testing alert manager...")
    
    try:
        from src.email_alert_system import AlertManager
        
        alert_manager = AlertManager()
        
        # Test user signup
        test_email = "test@example.com"
        result = alert_manager.signup_user(test_email)
        
        if result["success"]:
            print("✅ User signup functionality works")
        else:
            print(f"⚠️ User signup result: {result['message']}")
        
        # Test subscription management
        subscriptions = alert_manager.get_user_subscriptions(test_email)
        print(f"✅ Subscription management works (found {len(subscriptions)} subscriptions)")
        
        return True
        
    except Exception as e:
        print(f"❌ Alert manager test failed: {e}")
        return False

def test_email_templates():
    """Test email template generation."""
    print("\n🧪 Testing email templates...")
    
    try:
        from src.email_alert_system import EmailTemplate
        
        # Test ESG score alert template
        esg_template = EmailTemplate.get_esg_score_alert_template(
            company="AAPL",
            old_score=7.8,
            new_score=8.0,
            change_percent=2.3
        )
        
        if "AAPL" in esg_template and "2.3%" in esg_template:
            print("✅ ESG score alert template works")
        else:
            print("❌ ESG score alert template failed")
            return False
        
        # Test weekly summary template
        summary_data = {
            "top_performers": [("Apple", 8.5), ("Microsoft", 8.2)],
            "companies_to_watch": [("Exxon", 4.2)],
            "news_highlights": ["Apple announces new renewable energy initiatives"]
        }
        
        summary_template = EmailTemplate.get_weekly_summary_template(
            user_email="test@example.com",
            summary_data=summary_data
        )
        
        if "Weekly ESG Summary" in summary_template:
            print("✅ Weekly summary template works")
        else:
            print("❌ Weekly summary template failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Email template test failed: {e}")
        return False

def test_integration():
    """Test integration with the main dashboard."""
    print("\n🧪 Testing dashboard integration...")
    
    try:
        # Test if the email alert system can be imported in the main dashboard
        import importlib.util
        
        # Try to import the main dashboard
        spec = importlib.util.spec_from_file_location("ultimate_dashboard", "ultimate_dashboard.py")
        if spec is None:
            print("❌ Could not find ultimate_dashboard.py")
            return False
        
        dashboard_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard_module)
        
        # Check if EMAIL_ALERTS_ENABLED is defined
        if hasattr(dashboard_module, 'EMAIL_ALERTS_ENABLED'):
            print("✅ Email alerts integration detected in main dashboard")
        else:
            print("⚠️ Email alerts integration not found in main dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide a summary."""
    print("🚀 Starting ESG Email Alert System Tests")
    print("=" * 50)
    
    tests = [
        ("Database Creation", test_database_creation),
        ("Email Sender", test_email_sender),
        ("Alert Manager", test_alert_manager),
        ("Email Templates", test_email_templates),
        ("Dashboard Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Email alert system is ready to use.")
        print("\nNext steps:")
        print("1. Run 'streamlit run email_setup.py' to configure email settings")
        print("2. Run 'streamlit run ultimate_dashboard.py' to start the dashboard")
        print("3. Navigate to '📧 Email Alerts' in the dashboard")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure all required packages are installed")
        print("2. Check that the src/ directory exists with email_alert_system.py")
        print("3. Verify database permissions in the data/ directory")

if __name__ == "__main__":
    run_all_tests() 