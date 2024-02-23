# SSL Certificate Expiry Checker

This script checks the SSL certificate expiry for a list of domains and sends an email if the certificate is going to expire in less than a specified number of days.

## Requirements

- Python 3
- The following Python packages: `subprocess`, `datetime`, `smtplib`, `email.mime.multipart`, `email.mime.text`, `argparse`, `ast`, `os`

## Installation

First, make sure you have Python 3 installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

Next, install the required Python packages. You can do this with the following command:

```bash
pip install subprocess datetime smtplib email.mime.multipart email.mime.text argparse ast os


Usage
To run the script, use the following command:

30
Replace the domain names, ports, email addresses, and number of days with your actual values.

The --domains argument is a list of tuples, where each tuple contains a domain name and a port number. The --sender_email argument is the email address that will send the notifications. The --recipient_emails and --cc_recipients arguments are lists of email addresses that will receive the notifications. The --days argument is the number of days to expiry that will trigger a notification.

Environment Variables
The script uses the SENDER_EMAIL_PASSWORD environment variable for the sender email's password. Make sure to set this environment variable in your system before running the script.

```
