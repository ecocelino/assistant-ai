# features/timer_reminder.py
import threading
import time
import re

# Need speak function to announce completion
_speak_func = None

def initialize(speak_function):
    """Allows the main script to pass the speak function."""
    global _speak_func
    _speak_func = speak_function

def timer_thread_internal(duration_seconds, reminder_text="Timer finished"):
    """Internal thread function."""
    if not _speak_func:
        print("Error: Speak function not initialized in timer module.")
        return
    print(f"[Timer Started: {duration_seconds}s for '{reminder_text}']")
    time.sleep(duration_seconds)
    _speak_func(reminder_text)
    print(f"[Timer Finished: '{reminder_text}']")

def reminder_thread_internal(duration_seconds, reminder_text="Reminder"):
    """Internal thread function."""
    if not _speak_func:
        print("Error: Speak function not initialized in timer module.")
        return
    print(f"[Reminder Set: {duration_seconds}s for '{reminder_text}']")
    time.sleep(duration_seconds)
    _speak_func(f"Reminder: {reminder_text}")
    print(f"[Reminder Finished: '{reminder_text}']")

def parse_duration(command):
    # Keep the parse_duration function code here (as defined before)
    command = command.lower()
    total_seconds = 0
    match_min_sec = re.search(r'(\d+)\s+(minute|minutes)\s+(?:and\s+)?(\d+)\s+(second|seconds)', command)
    if match_min_sec:
        minutes = int(match_min_sec.group(1)); seconds = int(match_min_sec.group(3))
        total_seconds = (minutes * 60) + seconds; return total_seconds
    match_minutes = re.search(r'(\d+)\s+(minute|minutes)', command)
    if match_minutes:
        total_seconds = int(match_minutes.group(1)) * 60
        match_seconds_also = re.search(r'(\d+)\s+(second|seconds)', command)
        if match_seconds_also: total_seconds += int(match_seconds_also.group(1))
        return total_seconds
    match_seconds = re.search(r'(\d+)\s+(second|seconds)', command)
    if match_seconds: total_seconds = int(match_seconds.group(1)); return total_seconds
    if "a minute and a half" in command: total_seconds = 90
    elif "a minute" in command or "one minute" in command: total_seconds = 60
    elif "half a minute" in command: total_seconds = 30
    return total_seconds if total_seconds > 0 else None

def handle_timer(command, speak):
    duration = parse_duration(command)
    if duration:
         reminder = f"Time's up! Your {duration // 60} minute{'s' if duration // 60 != 1 else ''} and {duration % 60} second{'s' if duration % 60 != 1 else ''} timer has finished." if duration >= 60 else f"Time's up! Your {duration} second{'s' if duration != 1 else ''} timer has finished."
         if "named" in command:
              try: reminder_subject = command.split("named", 1)[1].split("for")[0].strip(); reminder = f"Your timer named {reminder_subject} is finished!"
              except IndexError: pass

         speak(f"Okay, setting a timer for {duration // 60} minutes and {duration % 60} seconds.")
         timer = threading.Thread(target=timer_thread_internal, args=(duration, reminder))
         timer.daemon = True; timer.start()
    else:
         speak("Sorry, I didn't understand the timer duration. Please say 'set a timer for 5 minutes' or 'timer for 30 seconds'.")

def handle_reminder(command, speak, listen):
    try:
        parts = command.split("remind me to", 1)[1].strip()
        task = ""; time_phrase = ""; duration = None

        if " in " in parts:
            task, time_phrase = parts.rsplit(" in ", 1)
            task = task.strip().replace(" please", "")
            duration = parse_duration(time_phrase)

        if duration and task:
            speak(f"Okay, I will remind you to {task} in {duration // 60} minutes and {duration % 60} seconds.")
            reminder_th = threading.Thread(target=reminder_thread_internal, args=(duration, task))
            reminder_th.daemon = True; reminder_th.start()
        elif task and not time_phrase:
             speak("Okay. When should I remind you?")
             time_command = listen() # Use passed-in listen function
             if time_command:
                 duration = parse_duration(time_command)
                 if duration:
                      speak(f"Got it. I'll remind you to {task} in {duration // 60} minutes and {duration % 60} seconds.")
                      reminder_th = threading.Thread(target=reminder_thread_internal, args=(duration, task))
                      reminder_th.daemon = True; reminder_th.start()
                 else: speak("Sorry, I didn't understand that time duration for the reminder.")
             else: speak("Okay, cancelling the reminder.")
        else: speak("Sorry, I couldn't understand the reminder. Please say 'remind me to [task] in [time]'.")

    except Exception as e:
        print(f"Reminder Error: {e}")
        speak("Sorry, I had trouble setting the reminder.")