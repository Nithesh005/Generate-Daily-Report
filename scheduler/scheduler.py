import schedule
import time
import requests
from datetime import datetime

def call_send_report_api():
    try:
        response = requests.get("http://localhost:5000/send-report")
        log_message = f"[{datetime.now()}] API called successfully - Status: {response.status_code}, Response: {response.text}\n"
    except Exception as e:
        log_message = f"[{datetime.now()}] Failed to call API: {e}\n"

    with open("daily_report_log.txt", "a") as log_file:
        log_file.write(log_message)

# Schedule the task for 6:30 PM daily
schedule.every().day.at("01:13").do(call_send_report_api)

while True:
    schedule.run_pending()
    time.sleep(60)  # check every minute
