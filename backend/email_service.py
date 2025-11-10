import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration - set these as environment variables for security
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USERNAME)

def send_shortlist_email(candidate_name, candidate_email, job_title):
    """
    Send a shortlist confirmation email to a candidate.
    Returns True if successful, False otherwise.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("Warning: Email credentials not configured. Skipping email.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = candidate_email
        msg['Subject'] = f'Congratulations! You\'ve been shortlisted for {job_title}'
        
        # Email body
        body = f"""
Dear {candidate_name or 'Candidate'},

Congratulations! We are pleased to inform you that you have been shortlisted for the position of {job_title}.

Our recruitment team was impressed with your qualifications and experience. We will be in touch soon with the next steps in the hiring process.

Thank you for your interest in joining our team.

Best regards,
Recruitment Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, candidate_email, text)
        server.quit()
        
        print(f"Email sent successfully to {candidate_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
