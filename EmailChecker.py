import imaplib
import smtplib
from datetime import datetime
import logging
import logging.handlers
import os

# Set up basic logging configuration
log_filename = 'email_count_log.txt'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a timed rotating file handler
handler = logging.handlers.TimedRotatingFileHandler(log_filename, when='D', interval=30, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.info("Starting the script")

def count_emails_today(username, password):
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(username, password)
            mail.select('inbox')
            date = datetime.now().strftime("%d-%b-%Y")
            typ, data = mail.search(None, f'(SENTSINCE {date})')
            email_count = len(data[0].split())
            logging.info(f"Emails counted: {email_count}")
            return email_count
    except Exception as e:
        logging.error(f"Error in count_emails_today: {str(e)}")
        return None

def send_text_message(emails_count, from_email, from_password, recipient_number):
    if emails_count is None:
        logging.error("Failed to send text message because email count is None")
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            today = datetime.now()
            day_of_week = today.strftime("%A")
            formatted_date = today.strftime("%m/%d/%Y")
            message = f"Subject: Email Count\n\nYou received {emails_count} emails on {day_of_week}, {formatted_date}."
            server.sendmail(from_email, recipient_number, message)
            logging.info("Text message sent successfully")
    except Exception as e:
        logging.error(f"Error in send_text_message: {str(e)}")

# Environment variables for user-specific settings
username = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS')
from_email = username
from_password = password
recipient_number = os.getenv('SMS_RECIPIENT')

# Function calls to count emails and send notification
emails_received = count_emails_today(username, password)
if emails_received is not None:
    send_text_message(emails_received, from_email, from_password, recipient_number)
else:
    logging.info("No email count retrieved; no message sent.")
