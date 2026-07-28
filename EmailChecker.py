"""Count today's Gmail inbox emails and send yourself the total as a text.

Connects to Gmail over IMAP, counts messages received today, and emails the
count to a carrier SMS gateway address (e.g. 1234567890@txt.att.net) so it
arrives as a text message.

Configuration is read from environment variables:
    EMAIL_USER     Gmail address to check (also used as the sender)
    EMAIL_PASS     Gmail app password (not your normal account password)
    SMS_RECIPIENT  Destination address, usually a carrier SMS gateway
"""

import imaplib
import logging
import logging.handlers
import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage

IMAP_HOST = "imap.gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
LOG_FILENAME = "email_count_log.txt"

logger = logging.getLogger(__name__)


def setup_logging():
    """Log to a file that rotates daily, keeping the last 7 days."""
    handler = logging.handlers.TimedRotatingFileHandler(
        LOG_FILENAME, when="D", interval=1, backupCount=7
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(handler)


def count_emails_today(username, password):
    """Return the number of inbox emails received today, or None on error."""
    try:
        with imaplib.IMAP4_SSL(IMAP_HOST) as mail:
            mail.login(username, password)
            mail.select("inbox")
            date = datetime.now().strftime("%d-%b-%Y")  # Format: DD-MMM-YYYY
            typ, data = mail.search(None, f'(ON "{date}")')
            if typ != "OK":
                logger.error("IMAP search failed: %s", typ)
                return None
            email_count = len(data[0].split())
            logger.info("Emails counted: %s", email_count)
            return email_count
    except imaplib.IMAP4.error as exc:
        logger.error("IMAP error: %s", exc)
        return None
    except Exception as exc:
        logger.error("Error in count_emails_today: %s", exc)
        return None


def send_text_message(email_count, from_email, from_password, recipient):
    """Email the count to a carrier SMS gateway so it arrives as a text."""
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(from_email, from_password)
            today = datetime.now()
            message = EmailMessage()
            message["Subject"] = "Email Count"
            message["From"] = from_email
            message["To"] = recipient
            message.set_content(
                f"You received {email_count} emails on "
                f"{today.strftime('%A')}, {today.strftime('%m/%d/%Y')}."
            )
            server.send_message(message)
            logger.info("Text message sent successfully")
            return True
    except smtplib.SMTPException as exc:
        logger.error("SMTP error: %s", exc)
    except Exception as exc:
        logger.error("Error in send_text_message: %s", exc)
    return False


def main():
    setup_logging()
    logger.info("Starting the script")

    username = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient = os.getenv("SMS_RECIPIENT")

    if not all([username, password, recipient]):
        logger.error("One or more environment variables are not set.")
        logger.error("EMAIL_USER: %s", "Set" if username else "Not Set")
        logger.error("EMAIL_PASS: %s", "Set" if password else "Not Set")
        logger.error("SMS_RECIPIENT: %s", "Set" if recipient else "Not Set")
        return 1

    # The recipient should be a carrier SMS gateway address,
    # e.g. '1234567890@txt.att.net'
    if "@" not in recipient:
        logger.error(
            "SMS_RECIPIENT is not an email-style address; expected something "
            "like 1234567890@txt.att.net"
        )
        return 1

    email_count = count_emails_today(username, password)
    if email_count is None:
        logger.info("No email count retrieved; no message sent.")
        return 1

    if not send_text_message(email_count, username, password, recipient):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
