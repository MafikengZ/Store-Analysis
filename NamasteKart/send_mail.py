import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from validations import Validate
from dataclasses import dataclass
from decouple import config
from datetime import datetime

# SMTP server configuration
smtp_server = config('SMTP_SERVER')
smtp_port = config('SMTP_PORT')
smtp_username = config('SMTP_USERNAME')
smtp_password = config('SMTP_PASSWORD')

@dataclass
class Email:
    # validations = Validate
    
    # Email configuration
    sender_email = 'tebogomafikeng@gmail.com'
    receiver_email = 'tebogomafikeng@gmail.com'
    subject =  f'validation {datetime.now().strftime("%Y%m%d")}'
    message = f'total {10} incoming files , {8} successsful files and {2}rejected files for that day.'
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    
    def send_email(self):
        # Add body to the email
        self.msg.attach(MIMEText(self.message, 'plain'))

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(self.msg)
                print('Email sent successfully.')
        except Exception as e:
            print(f'Error sending email: {str(e)}')