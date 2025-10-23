# features/wikipedia_search.py
import wikipediaapi
from features.calculator import parse_calculation # Import check function

# Moved config here
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent=f'VenusAssistant/1.0 (YourEmail@example.com)' # <-- Replace email
)

def handle_wikipedia_search(command, speak, listen):
    # Check if it looks like a calculation first
    if parse_calculation(command):
        # Let the calculator handle it, return False to indicate not handled here
        return False

    search_term = ""
    try:
        # Keep the robust extraction logic here (as defined before)
        processed_command = command.replace("venus", "").strip() # Use assistant_name var?
        triggers = ["wikipedia for", "on wikipedia", "look up", "search wikipedia for", "what is", "who is", "tell me about"]
        found_trigger = False
        for trigger in triggers:
            if processed_command.startswith(trigger + " "):
                search_term = processed_command.split(trigger + " ", 1)[1]; found_trigger = True; break
            if " on wikipedia" in processed_command and trigger in processed_command.split(" on wikipedia")[0]:
                 parts = processed_command.split(" on wikipedia")[0]; search_term = parts.replace(trigger,"").strip(); found_trigger = True; break
        if not found_trigger:
             leading_words = ["search for", "look up", "define", "explain"]
             temp_command = processed_command
             for word in leading_words:
                 if temp_command.startswith(word + " "): temp_command = temp_command.split(word + " ", 1)[1]
             search_term = temp_command.replace(" on wikipedia", "").strip()
        search_term = search_term.replace(" please", "").replace("?", "").strip()

        if not search_term:
             speak("What topic would you like me to look up on Wikipedia?")
             term_command = listen() # Use passed-in listen function
             search_term = term_command if term_command else None

        if search_term:
             speak(f"Searching Wikipedia for {search_term}...")
             page = wiki_wiki.page(search_term)
             if page.exists():
                 summary_sentences = page.summary.split('.')
                 num_sentences = min(len(summary_sentences), 3)
                 response_summary = ". ".join(s for s in summary_sentences[:num_sentences] if s).strip()
                 speak("According to Wikipedia: " + response_summary + "." if response_summary else page.summary)
             else:
                 speak(f"Sorry, I couldn't find a Wikipedia page for {search_term}.")
        elif search_term is None:
             speak("Okay, cancelling the search.")
        return True # Handled the command (even if search failed)

    except Exception as e:
        print(f"Wikipedia Error: {e}")
        speak("Sorry, I encountered an error while searching Wikipedia.")
        return True # Still handled (tried and failed)