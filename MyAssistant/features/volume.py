# features/volume.py
import subprocess
import re

def handle_volume(command, speak):
    try:
        if "volume up" in command or "increase volume" in command:
            subprocess.run(['amixer', '-q', 'set', 'Master', '5%+'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak("Volume increased.")
        elif "volume down" in command or "decrease volume" in command:
            subprocess.run(['amixer', '-q', 'set', 'Master', '5%-'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak("Volume decreased.")
        elif "set volume to" in command:
            match = re.search(r'set volume to (\d+)', command)
            if match:
                percent = match.group(1)
                if 0 <= int(percent) <= 100:
                    subprocess.run(['amixer', '-q', 'set', 'Master', f'{percent}%'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speak(f"Volume set to {percent} percent.")
                else: speak("Please specify a volume percentage between 0 and 100.")
            else: speak("Please specify a percentage, like 'set volume to 50'.")
        elif "mute volume" in command or "mute sound" in command:
            subprocess.run(['amixer', '-q', 'set', 'Master', 'mute'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak("Volume muted.")
        elif "unmute volume" in command or "unmute sound" in command:
            subprocess.run(['amixer', '-q', 'set', 'Master', 'unmute'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak("Volume unmuted.")
        else:
            # Should not happen if called correctly, but as a fallback
            speak("Sorry, I didn't understand the volume command.")
    except FileNotFoundError:
         speak("Sorry, the 'amixer' command wasn't found. Volume control unavailable.")
    except Exception as e:
        print(f"Volume Control Error: {e}")
        speak("Sorry, I couldn't adjust the volume.")