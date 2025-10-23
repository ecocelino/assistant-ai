# features/weather.py
import requests

# Moved config here, could also be passed from main or a config file
WEATHERAPI_KEY = "b28d603026574cacaab60733252210" # <-- PASTE YOUR KEY HERE
DEFAULT_CITY = "Marilao"

def handle_weather(command, speak):
    try:
        city = DEFAULT_CITY
        if "in " in command:
            potential_city = command.split("in ", 1)[1].strip()
            city = potential_city.split(" please")[0].replace("?", "").strip()
        elif "for " in command:
             potential_city = command.split("for ", 1)[1].strip()
             city = potential_city.split(" please")[0].replace("?", "").strip()

        speak(f"Getting the current weather for {city}...")
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = base_url + "key=" + WEATHERAPI_KEY + "&q=" + city + "&aqi=no"

        response = requests.get(complete_url, timeout=10)
        response.raise_for_status()
        weather_data = response.json()

        if "current" in weather_data:
            current_data = weather_data["current"]
            temp_c = current_data.get("temp_c")
            feelslike_c = current_data.get("feelslike_c")
            humidity = current_data.get("humidity")
            condition = current_data.get("condition", {}).get("text", "No description available")

            if temp_c is not None and feelslike_c is not None:
                 speak(f"The temperature in {city} is {temp_c:.0f} degrees Celsius, and it feels like {feelslike_c:.0f} degrees.")
            elif temp_c is not None:
                 speak(f"The temperature in {city} is {temp_c:.0f} degrees Celsius.")
            if humidity is not None:
                speak(f"The humidity is {humidity} percent.")
            speak(f"The current condition is {condition}.")
        elif "error" in weather_data:
             error_message = weather_data.get("error", {}).get("message", "Unknown error")
             print(f"WeatherAPI Error: {error_message}")
             speak(f"Sorry, I couldn't find the weather for {city}. The service reported: {error_message}")
        else:
             speak(f"Sorry, I received an unexpected response for {city}.")

    except requests.exceptions.Timeout:
         print("Weather request timed out.")
         speak("Sorry, the weather service took too long to respond.")
    except requests.exceptions.RequestException as e:
         print(f"Network error fetching weather: {e}")
         speak("Sorry, I couldn't connect to the weather service.")
    except Exception as e:
        print(f"Weather Processing Error: {e}")
        speak("Sorry, I had trouble processing the weather information.")