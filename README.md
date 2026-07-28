# MailChecker

Counts how many emails landed in a Gmail inbox today and texts you the total.

The script connects to Gmail over IMAP, counts messages received on the current
day, and sends the count through Gmail SMTP to a **carrier SMS gateway** address
(e.g. `1234567890@txt.att.net`), so the notification arrives on your phone as a
regular text message — no SMS API or paid service required.

## Features

- Counts inbox emails received today via IMAP.
- Delivers the count as an SMS using your carrier's email-to-text gateway.
- All configuration via environment variables — no credentials in the code.
- Logs to `email_count_log.txt`, rotating daily and keeping the last 7 days.

## Examples

![Example](https://i.imgur.com/9XnHSnV.jpeg)
![logExample](https://i.imgur.com/kBp8rRB.png)

## Prerequisites

- Python 3.8+ (uses only the standard library — nothing to `pip install`)
- IMAP enabled in your Gmail settings (Settings → Forwarding and POP/IMAP)
- A [Gmail app password](https://support.google.com/accounts/answer/185833)
  (regular account passwords won't work with 2FA enabled)
- Your carrier's SMS gateway domain, for example:
  | Carrier | Gateway |
  |---|---|
  | AT&T | `number@txt.att.net` |
  | Verizon | `number@vtext.com` |
  | T-Mobile | `number@tmomail.net` |

## Setup

Set three environment variables:

```bash
# macOS / Linux
export EMAIL_USER='your_email@gmail.com'
export EMAIL_PASS='your-app-password'
export SMS_RECIPIENT='1234567890@txt.att.net'
```

```powershell
# Windows (PowerShell)
$env:EMAIL_USER = 'your_email@gmail.com'
$env:EMAIL_PASS = 'your-app-password'
$env:SMS_RECIPIENT = '1234567890@txt.att.net'
```

## Usage

```bash
python EmailChecker.py
```

Schedule it (cron on macOS/Linux, Task Scheduler on Windows) to get a daily
end-of-day text with your inbox count.
