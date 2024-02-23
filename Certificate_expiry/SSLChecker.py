import subprocess
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import ast
import os

# SSLChecker class
class SSLChecker:
    # Initialize SSLChecker with domain, port, sender email, recipient emails, cc recipients, and days
    def __init__(self, domain, port, sender_email, recipient_emails, cc_recipients, days):
        self.domain = domain
        self.port = port
        self.sender_email = sender_email
        self.recipient_emails = recipient_emails
        self.cc_recipients = cc_recipients
        self.days = days

    # Method to check SSL expiry
    def check_ssl_expiry(self):
        # Command to get SSL certificate information
        cmd = f'echo | openssl s_client -servername {self.domain} -connect {self.domain}:{self.port} 2>/dev/null | openssl x509 -noout -dates'
        output = subprocess.check_output(cmd, shell=True).decode()    

        # Extract expiry date from the output
        expiry_line = [line for line in output.split('\n') if 'notAfter' in line][0]
        expiry_date_str = expiry_line.split('=')[1]
  
        # Convert expiry date to datetime object
        expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')  
        # Calculate days to expiry
        days_to_expire = (expiry_date - datetime.utcnow()).days

        return days_to_expire

    # Method to send email
    def send_email(self,days_to_expire):
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(self.recipient_emails)
        msg['Cc'] = ', '.join(self.cc_recipients)
        msg['Subject'] = f'SSL Certificate Expiry Warning for {self.domain}'

        # Email body
        body = f'The SSL certificate for {self.domain} is going to expire in {days_to_expire} days.'
        msg.attach(MIMEText(body, 'plain'))

        # Setup SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Login to the server
        server.login(self.sender_email, os.getenv('SENDER_EMAIL_PASSWORD'))  # replace 'password' with the actual password

        # Convert message to string and send email
        text = msg.as_string()
        server.sendmail(self.sender_email, self.recipient_emails + self.cc_recipients, text)
        server.quit()

# Main function
if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Check SSL expiry for domains.")
    parser.add_argument('--domains', type=str, help='List of domains and ports')
    parser.add_argument('--sender_email', type=str, help='Sender email')
    parser.add_argument('--recipient_emails', type=str, help='List of recipients email')
    parser.add_argument('--cc_recipients', type=str, help='List of cc emails')
    parser.add_argument('--days', type=int, help='No of days to expire')

    # Parse arguments
    args = parser.parse_args()

    # Convert string arguments to Python objects
    domains = ast.literal_eval(args.domains)
    sender_email = args.sender_email
    recipient_emails = ast.literal_eval(args.recipient_emails)
    cc_recipients = ast.literal_eval(args.cc_recipients)
    days = args.days

    # For each domain, check SSL expiry and send email if necessary
    for domain, port in domains:
        ssl_checker = SSLChecker(domain, port, sender_email, recipient_emails, cc_recipients, days)
        days_to_expire = ssl_checker.check_ssl_expiry()
        if days_to_expire < days:
            ssl_checker.send_email(days_to_expire)
