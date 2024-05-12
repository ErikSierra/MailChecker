# Email Tracker

## Project Overview
Email Tracker is a Python script that counts the number of emails received in a Gmail inbox for the current day and sends an SMS notification with the count. This script utilizes `imaplib` for interacting with the Gmail IMAP server and `smtplib` for sending SMS messages via email.

## Features
- Counts emails received in the inbox for the current day.
- Sends an SMS with the email count.
- Uses logging to keep track of operations and errors.

## Logging
Logs are written to email_count_log.txt and are rotated every 30 days with a backup of the last period kept.

## Prerequisites
Before you run this script, ensure you have Python installed on your system. You also need to enable IMAP access in your Gmail settings and configure your account for less secure apps (or better, use OAuth2 authentication).

## Installation
1. Clone this repository or download the files to your local machine.
2. Install the required Python libraries by running:
   ```bash
   pip install imaplib smtplib datetime logging
3. Set up environment variables for your Gmail username and password (recommended for security reasons):
   ```bash
   export EMAIL_USER='your_email@gmail.com'
   export EMAIL_PASS='yourapppassword'
   
## Configuration
Update the script with your specific details where necessary, particularly in setting up the recipient of the SMS notification and the sender details.

## Usage
Run the script using Python from the command line:
   ```bash
   export EMAIL_USER='your_email@gmail.com'
   export EMAIL_PASS='yourapppassword'





