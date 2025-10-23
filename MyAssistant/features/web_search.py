# features/web_search.py
# Note: webbrowser requires a GUI, so we just print the URL on the server

def handle_google_search(command, speak, listen):
    search_query = command.split("for", 1)[1].strip().replace("?", "").replace(" please", "")
    if search_query:
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        speak(f"Searching Google for {search_query}.")
        print(f"[Action: Would open browser to: {search_url}]")
    else:
        speak("What would you like me to search Google for?")
        followup_query = listen() # Need listen function passed in
        if followup_query:
           search_url = f"https://www.google.com/search?q={followup_query.replace(' ', '+')}"
           speak(f"Searching Google for {followup_query}.")
           print(f"[Action: Would open browser to: {search_url}]")
        else:
           speak("Okay, cancelling search.")


def handle_youtube_search(command, speak, listen):
    search_query = command.split("for", 1)[1].strip().replace("?", "").replace(" please", "")
    if search_query:
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        speak(f"Searching YouTube for {search_query}.")
        print(f"[Action: Would open browser to: {search_url}]")
    else:
        speak("What would you like me to search YouTube for?")
        # Similar follow-up logic as Google search if desired