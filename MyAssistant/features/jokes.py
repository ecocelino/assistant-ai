# features/jokes.py
import pyjokes

def handle_joke(command, speak):
    speak("Okay, here comes a joke...")
    try:
        joke = pyjokes.get_joke(language='en', category='neutral')
        speak(joke)
    except Exception as e:
         print(f"Joke Error: {e}")
         speak("Sorry, I couldn't fetch a joke right now.")