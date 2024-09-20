import imaplib
import smtplib
from email.message import EmailMessage
from datetime import datetime
import logging
import logging.handlers
import os

# Set up basic logging configuration
log_filename = 'email_count_log.txt'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a timed rotating file handler
handler = logging.handlers.TimedRotatingFileHandler(
    log_filename, when='D', interval=1, backupCount=7
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Avoid adding multiple handlers if the script runs multiple times
if not logger.handlers:
    logger.addHandler(handler)

logging.info("Starting the script")

def count_emails_today(username, password):
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(username, password)
            mail.select('inbox')
            date = datetime.now().strftime("%d-%b-%Y")  # Format: DD-MMM-YYYY
            typ, data = mail.search(None, f'(ON "{date}")')
            if typ != 'OK':
                logging.error(f"IMAP search failed: {typ}")
                return None
            email_count = len(data[0].split())
            logging.info(f"Emails counted: {email_count}")
            return email_count
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error in count_emails_today: {str(e)}")
        return None

def send_text_message(emails_count, from_email, from_password, recipient_email):
    if emails_count is None:
        logging.error("Failed to send text message because email count is None")
        return
    try:
        # Create an SSL context and connect to the SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, from_password)
            today = datetime.now()
            day_of_week = today.strftime("%A")
            formatted_date = today.strftime("%m/%d/%Y")
            message = EmailMessage()
            message['Subject'] = 'Email Count'
            message['From'] = from_email
            message['To'] = recipient_email
            message.set_content(
                f"You received {emails_count} emails on {day_of_week}, {formatted_date}."
            )
            server.send_message(message)
            logging.info("Text message sent successfully")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {str(e)}")
    except Exception as e:
        logging.error(f"Error in send_text_message: {str(e)}")

# Environment variables for user-specific settings
username = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS')
from_email = username
from_password = password
recipient_number = os.getenv('SMS_RECIPIENT')

# Verify that all required environment variables are set
if not all([username, password, recipient_number]):
    logging.error("One or more environment variables are not set.")
    logging.error(f"EMAIL_USER: {username}")
    logging.error(f"EMAIL_PASS: {'Set' if password else 'Not Set'}")
    logging.error(f"SMS_RECIPIENT: {recipient_number}")
    exit(1)

# Ensure recipient_number includes the carrier SMS gateway domain
# Example: '1234567890@txt.att.net'
if '@' not in recipient_number:
    logging.error("Recipient number is not properly formatted with SMS gateway domain.")
    recipient_number = None

# Function calls to count emails and send notification
emails_received = count_emails_today(username, password)
if emails_received is not None and recipient_number:
    send_text_message(emails_received, from_email, from_password, recipient_number)
else:
    logging.info("No email count retrieved or recipient number invalid; no message sent.")
