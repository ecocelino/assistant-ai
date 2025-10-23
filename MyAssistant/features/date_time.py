# features/date_time.py
import datetime

def handle_date_time(command, speak):
    now_time = datetime.datetime.now().strftime("%I:%M %p")
    today_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {today_date}, and the current time is {now_time}.")

def handle_time_query(command, speak):
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}.")

def handle_date_query(command, speak):
    today = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {today}.")