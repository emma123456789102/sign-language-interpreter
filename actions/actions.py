# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import requests
from actions.letter_quiz_actions import ActionLetterQuizCheckLetter
from actions.word_quiz_actions import ActionWordQuizCheckLetter

class ActionReturnCurrentGesture(Action):
    def name(self):
        return "action_gesture_return_current"

    def run(self, dispatcher, tracker, domain):
        try:
            response = requests.get("http://localhost:5000/gesture")
            gesture = response.json().get("gesture", "unknown")
            dispatcher.utter_message(text=f"Your current gesture looks like: {gesture}.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't get your current gesture.")
        return []

class ActionReturnCurrentEmotion(Action):
    def name(self):
        return "action_emotion_return_current"

    def run(self, dispatcher, tracker, domain):
        try:
            response = requests.get("http://localhost:5000/emotion")
            emotion = response.json().get("emotion", "unknown")
            dispatcher.utter_message(text=f"Your current emotion seems to be: {emotion}.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't get your current emotion.")
        return []
    
class ActionReturnCurrentState(Action):
    def name(self):
        return "action_state_return_current"

    def run(self, dispatcher, tracker, domain):
        try:
            response = requests.get("http://localhost:5000/gesture")
            gesture = response.json().get("gesture", "unknown")
            emotion = response.json().get("emotion", "unknown")
            dispatcher.utter_message(text=f"Your current gesture looks like: {gesture}, and your emotion seems to be: {emotion}.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the state.")
        return []
    
class ActionCheckLetterByQuizMode(Action):
    def name(self):
        return "action_check_letter_by_quiz_mode"

    async def run(self, dispatcher, tracker, domain):
        quiz_mode = tracker.get_slot("quiz_mode")

        if quiz_mode == "letter":
            return ActionLetterQuizCheckLetter().run(dispatcher, tracker, domain)
        elif quiz_mode == "word":
            return ActionWordQuizCheckLetter().run(dispatcher, tracker, domain)
        else:
            dispatcher.utter_message("[RASA] Quiz not running.")
            return []