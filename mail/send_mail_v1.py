import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your org details
smtp_server = "smtp.office365.com"
port = 587  # TLS
sender_email = "nithish@dreaminfinity.in"
receiver_email = "nitheshwaran003@gmail.com"
password = "Nithesh#di1"

# Build the message
msg = MIMEMultipart("alternative")
msg["Subject"] = "🗓️ Daily Git Commit Report"
msg["From"] = sender_email
msg["To"] = receiver_email

# Add plain text report
text_part = MIMEText("final_report", "plain")
msg.attach(text_part)

# Send email using TLS
try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", e)
