import speech_recognition as sr
import pyttsx3
import requests
import time
import sys

tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[2].id)

recognizer = sr.Recognizer()

RASA_REST_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"
RASA_STATUS_ENDPOINT = "http://localhost:5005/status"

def rasa_available():
    try:
        response = requests.get(RASA_STATUS_ENDPOINT)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def listen():
    with sr.Microphone() as source:
        print("Speak now:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("I didn't catch that. Try again.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""

def speak(text):
    print(f"Rasa says: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def send_to_rasa(user_input):
    payload = {"sender": "user", "message": user_input}
    try:
        response = requests.post(RASA_REST_ENDPOINT, json=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to Rasa server: {e}")
        return []

print("Waiting for Rasa server to start...")
while not rasa_available():
    time.sleep(2)

print("Rasa server is up. Starting speech interface...")

try:
    while True:
        if not rasa_available():
            print("Rasa server stopped. Exiting speech handler.")
            sys.exit(0)

        user_input = listen()
        if user_input:
            messages = send_to_rasa(user_input)
            for msg in messages:
                response= msg.get("text")
                if response:
                    speak(response)
except KeyboardInterrupt:
    print("\nExiting speech handler.")
    sys.exit(0)
