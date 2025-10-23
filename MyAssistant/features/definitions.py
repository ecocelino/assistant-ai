# features/definitions.py
import requests

def handle_definition(command, speak, listen):
    try:
        word = ""
        if command.startswith("define "):
             word = command.split("define ", 1)[1].strip().replace("?", "").split(" ")[0]
        elif "what does" in command and "mean" in command:
             parts = command.split("what does", 1)[1].split("mean")[0].strip()
             word = parts
        else:
             speak("What word would you like me to define?")
             word_command = listen() # Use passed-in listen function
             word = word_command if word_command else None

        if word:
            speak(f"Looking up the definition for {word}...")
            api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                definitions = response.json()
                first_meaning = definitions[0].get('meanings', [{}])[0]
                first_definition = first_meaning.get('definitions', [{}])[0].get('definition')
                part_of_speech = first_meaning.get('partOfSpeech', '')
                if first_definition:
                     speak(f"As a {part_of_speech}, {word} means: {first_definition}")
                else: speak(f"I found an entry for {word}, but couldn't get a clear definition.")
            elif response.status_code == 404: speak(f"Sorry, I couldn't find a definition for {word}.")
            else: speak("Sorry, I couldn't reach the dictionary service right now.")
        elif word is None: speak("Okay, cancelling definition lookup.")

    except requests.exceptions.RequestException as e:
         print(f"Dictionary API Network Error: {e}")
         speak("Sorry, I couldn't connect to the dictionary service.")
    except (IndexError, KeyError, TypeError) as e:
         print(f"Dictionary API Parsing Error: {e}")
         speak(f"Sorry, I found a definition for {word}, but couldn't process it correctly.")
    except Exception as e:
        print(f"Definition Error: {e}")
        speak("Sorry, I encountered an error looking up the definition.")