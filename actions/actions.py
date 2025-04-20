# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionReturnCurrentGesture(Action):
    def name(self):
        return "action_gesture_return_current"

    def run(self, dispatcher, tracker, domain):
        try:
            response = requests.get("http://localhost:5000/gesture")
            gesture = response.json().get("gesture", "unknown")
            dispatcher.utter_message(text=f"The current gesture is: {gesture}.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the gesture.")
        return []
