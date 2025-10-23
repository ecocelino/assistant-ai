# features/calculator.py
import re
from num2words import num2words

def parse_calculation(command):
    # Keep the parse_calculation function code here (as defined before)
    command = command.lower().replace("what's", "what is")
    replacements = {" plus ": "+", " add ": "+", " minus ": "-", " subtract ": "-", " take away ": "-", " times ": "*", " multiplied by ": "*", " divided by ": "/", " over ": "/", " point ": ".", " dot ": "."}
    num_words = {"zero": "0", "one": "1", "two": "2", "to": "2", "too": "2", "three": "3", "four": "4", "for": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}
    processed_command = command
    for word, digit in num_words.items(): processed_command = re.sub(r'\b' + word + r'\b', digit, processed_command)
    for word, symbol in replacements.items(): processed_command = processed_command.replace(word, symbol)
    match = re.search(r'(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)', processed_command)
    if match:
        num1_str, operator, num2_str = match.groups()
        try: return float(num1_str), operator, float(num2_str)
        except ValueError: return None
    if processed_command.startswith("what is "):
        processed_command = processed_command[len("what is "):]
        match = re.search(r'(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)', processed_command)
        if match:
            num1_str, operator, num2_str = match.groups()
            try: return float(num1_str), operator, float(num2_str)
            except ValueError: return None
    return None

def handle_calculation(command, speak):
    calculation = parse_calculation(command)
    if calculation:
        num1, operator, num2 = calculation
        result = None
        try:
            if operator == '+': result = num1 + num2
            elif operator == '-': result = num1 - num2
            elif operator == '*': result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    speak("Sorry, division by zero is not allowed.")
                    return
                result = num1 / num2

            if result is not None:
                num1_str = str(int(num1)) if num1 == int(num1) else f"{num1:.2f}"
                num2_str = str(int(num2)) if num2 == int(num2) else f"{num2:.2f}"
                if result == int(result): result_str = str(int(result))
                else: result_str = f"{result:.2f}"
                speak(f"The result of {num1_str} {operator} {num2_str} is {result_str}")

        except Exception as e:
            print(f"Calculation Error: {e}")
            speak("Sorry, I encountered an error performing that calculation.")
    else:
        speak("Sorry, I couldn't understand the calculation. Please say it clearly, like 'calculate 15 times 4'.")