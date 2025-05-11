import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_daily_report(report_content):
    """
    Function to send the daily git commit report via email.
    
    :param report_content: The report content to be sent in the email body
    """
    print("📧 Mailing Process Started... ✉️")
    # Static email configuration
    sender_email = "terionorganization@gmail.com"
    receiver_email = ["nitheshwaran003@gmail.com", "nithish@dreaminfinity.in","nithish@ezbillpay.in"]
    password = "imkq rydg xtla lvmx"  # Use App Password if Gmail

    # Setup the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🗓️ Daily Git Commit Report v1"
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_email)

    # Attach the plain text report
    text_part = MIMEText(report_content, "plain")
    msg.attach(text_part)

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


# Example usage of the function
# report_content = "Your daily Git commit report goes here..."  # Replace with the actual content of your report

# # Call the function to send the email
# send_daily_report(report_content)
