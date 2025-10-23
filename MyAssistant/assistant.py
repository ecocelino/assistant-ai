# assistant.py (Main Script)

# --- Core Libraries ---
import speech_recognition as sr
import datetime
import os
import struct
import time
import pygame # Keep pygame init and quit here

# --- Feature Libraries (Import handlers) ---
from features import basic_conversation
from features import date_time
from features import web_search
from features import weather
from features import calculator
from features import wikipedia_search
from features import jokes
from features import timer_reminder
from features import definitions
from features import volume

# --- NEW IMPORTS FOR gTTS ---
from gtts import gTTS

# --- 1. Assistant Name ---
assistant_name = "Venus"

# --- 2. Initialize Pygame Mixer ---
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing pygame mixer: {e}")
    print("Audio playback might not work.")

# --- 3. Text-to-Speech (TTS) using gTTS + Pygame ---
# (Speak function remains here as it's core)
def speak(text):
    """Converts text to speech using gTTS and plays it via pygame mixer."""
    print(f"{assistant_name}: {text}")
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        temp_audio_file = "temp_venus_speech.mp3"
        tts.save(temp_audio_file)
        try:
            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): time.sleep(0.1)
        except Exception as e: print(f"Error playing audio with pygame: {e}")
        finally:
             if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
             pygame.mixer.music.unload(); time.sleep(0.1)
        try: os.remove(temp_audio_file)
        except OSError as e: print(f"Error removing temporary file: {e}")
    except Exception as e:
        print(f"Error during gTTS speech synthesis or pygame playback: {e}")
        print("(Could not play synthesized speech)")

# --- Initialize Timer/Reminder module with speak function ---
timer_reminder.initialize(speak)

# --- 4. Speech-to-Text (STT) Setup ---
# (listen_for_command function remains here)
r = sr.Recognizer()
def listen_for_command():
    """Listens via microphone, recognizes speech using Google Web Speech API."""
    with sr.Microphone() as source:
        print(f"\n{assistant_name} is listening...")
        r.pause_threshold = 1
        try: r.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e: print(f"Could not adjust for ambient noise: {e}")
        try: audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError: print("Listening timed out."); return None
        except Exception as e: print(f"Error during listening: {e}"); return None
    try:
        print("Recognizing..."); command = r.recognize_google(audio).lower()
        print(f"You said: {command}\n"); return command
    except sr.UnknownValueError: print("Sorry, I did not understand that."); return None
    except sr.RequestError as e: print(f"Could not request results; {e}"); speak("Speech service connection issue."); return None
    except Exception as e: print(f"Recognition error: {e}"); return None

# --- 5. Command Processing Logic (Dispatcher) ---
def process_command(command):
    """Determines action based on recognized command keywords and calls feature handlers."""
    command_handled = True # Flag to track if any feature handled the command

    # Order matters: More specific or potentially overlapping triggers first
    if "calculate" in command or "compute" in command or ("what is" in command and any(op in command for op in ["plus", "add", "minus", "subtract", "take away", "times", "multiplied by", "divided by", "over", "+", "-", "*", "/"])):
        calculator.handle_calculation(command, speak)
    elif "timer for" in command or "set a timer" in command:
        timer_reminder.handle_timer(command, speak)
    elif "remind me to" in command:
        timer_reminder.handle_reminder(command, speak, listen_for_command) # Pass listen for follow-up
    elif "volume" in command or "mute" in command: # Broad trigger for volume
        volume.handle_volume(command, speak)
    elif "weather" in command:
        weather.handle_weather(command, speak)
    elif "joke" in command:
        jokes.handle_joke(command, speak)
    elif "define" in command or ("what does" in command and "mean" in command):
         definitions.handle_definition(command, speak, listen_for_command) # Pass listen
    elif "wikipedia" in command or "look up" in command or "search wikipedia for" in command or ("what is" in command) or ("who is" in command) or ("tell me about" in command):
         # Let the wikipedia handler do the check for calculation overlap
         command_handled = wikipedia_search.handle_wikipedia_search(command, speak, listen_for_command)
    elif "google search for" in command or "search google for" in command:
         web_search.handle_google_search(command, speak, listen_for_command)
    elif "youtube search for" in command or "search youtube for" in command:
         web_search.handle_youtube_search(command, speak, listen_for_command)
    elif "date and time" in command:
        date_time.handle_date_time(command, speak)
    elif "time" in command:
        date_time.handle_time_query(command, speak)
    elif "date" in command:
        date_time.handle_date_query(command, speak)
    elif f"hello {assistant_name.lower()}" in command or f"hi {assistant_name.lower()}" in command or command.strip() == "hello" or command.strip() == "hi":
        basic_conversation.handle_greeting(command, speak)
    elif "your name" in command:
        basic_conversation.handle_name_query(command, speak)
    else:
        command_handled = False # No specific feature matched

    # Default fallback if no feature handled the command
    if not command_handled:
         # Check again if it looked like a failed calculation before giving generic failure
        is_potential_calculation = "calculate" in command or "compute" in command or ("what is" in command and any(op in command for op in ["plus", "add", "minus", "subtract", "take away", "times", "multiplied by", "divided by", "over", "+", "-", "*", "/"]))
        if not is_potential_calculation:
             speak("Sorry, I don't understand that command yet.")


# --- 6. Main Execution Loop ---
if __name__ == "__main__":
    speak(f"Hello, I'm {assistant_name}, your personal assistant. How can I help?")
    while True:
        command = listen_for_command()
        if command:
            exit_phrases = ["exit", "quit", "stop listening", f"goodbye {assistant_name.lower()}", "shutdown", "turn off", "bye venus"]
            if any(phrase in command for phrase in exit_phrases):
                speak("Goodbye! Have a great day.")
                pygame.mixer.quit() # Clean up pygame mixer
                break
            process_command(command)
        # else:
        #    time.sleep(0.1) # Optional pause if no command heard