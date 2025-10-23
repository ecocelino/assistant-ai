# features/basic_conversation.py
import datetime # May be needed if adding more time-sensitive greetings

assistant_name = "Sofia" # Define name here or pass it in

def handle_greeting(command, speak):
    speak("Hello! How can I assist you today?")

def handle_name_query(command, speak):
    speak(f"My name is {assistant_name}.")

# Add more simple back-and-forth conversation handlers here if needed