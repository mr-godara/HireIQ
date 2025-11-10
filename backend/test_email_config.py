"""
Test script to verify email configuration without sending actual emails
"""
import os

def test_email_config():
    """Test if email environment variables are configured"""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Check environment variables
    smtp_server = os.environ.get('SMTP_SERVER', '')
    smtp_port = os.environ.get('SMTP_PORT', '')
    smtp_username = os.environ.get('SMTP_USERNAME', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('FROM_EMAIL', '')
    
    print("\n📧 Email Configuration Status:\n")
    
    configs = [
        ("SMTP_SERVER", smtp_server, "smtp.gmail.com"),
        ("SMTP_PORT", smtp_port, "587"),
        ("SMTP_USERNAME", smtp_username, "your-email@gmail.com"),
        ("SMTP_PASSWORD", smtp_password, "your-app-password"),
        ("FROM_EMAIL", from_email, "your-email@gmail.com")
    ]
    
    all_configured = True
    
    for name, value, example in configs:
        if value:
            print(f"✅ {name}: Configured")
            if name != 'SMTP_PASSWORD':  # Don't print password
                print(f"   Value: {value}")
        else:
            print(f"❌ {name}: Not configured")
            print(f"   Example: {example}")
            all_configured = False
        print()
    
    print("=" * 60)
    
    if all_configured:
        print("✅ All email settings are configured!")
        print("\nEmail notifications will be sent when shortlisting candidates.")
        print("\nTo test email functionality:")
        print("1. Start the Flask server")
        print("2. Upload a resume with a valid email")
        print("3. Create a job and view matches")
        print("4. Click 'Shortlist' and choose 'OK' to send email")
    else:
        print("⚠️  Email is not fully configured.")
        print("\nThe application will still work, but emails won't be sent.")
        print("\nTo configure email, set these environment variables:")
        print("\nPowerShell:")
        print('$env:SMTP_SERVER="smtp.gmail.com"')
        print('$env:SMTP_PORT="587"')
        print('$env:SMTP_USERNAME="your-email@gmail.com"')
        print('$env:SMTP_PASSWORD="your-app-password"')
        print('$env:FROM_EMAIL="your-email@gmail.com"')
        print("\nSee backend/EMAIL_SETUP.md for detailed instructions.")
    
    print("=" * 60)
    return all_configured

if __name__ == "__main__":
    test_email_config()
