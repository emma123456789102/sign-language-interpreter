import random
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

def get_current_gesture():
    try:
        response = requests.get("http://localhost:5000/gesture")
        return response.json().get("gesture")
    except:
        return None

class ActionStartQuiz(Action):
    def name(self):
        return "action_quiz_start"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Starting quiz.")
        quiz_letters = random.sample([chr(i) for i in range(65, 91)], 5)  # Generate 5 random letters A-Z
        first_letter = quiz_letters[0]

        dispatcher.utter_message(text="Let's get quizzy.")
        dispatcher.utter_message(text=f"First, sign '{first_letter}'. Say 'Ready' or 'Check me' when ready.")

        return [
            SlotSet("quiz_letters", quiz_letters),
            SlotSet("quiz_current_letter", first_letter),
            SlotSet("quiz_index", 0),
            SlotSet("quiz_score", 0)
        ]

class ActionCheckQuizLetter(Action):
    def name(self):
        return "action_quiz_check_letter"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Checking quiz letter.")
        quiz_letters = tracker.get_slot("quiz_letters") or []
        index = int(tracker.get_slot("quiz_index") or 0)
        score = int(tracker.get_slot("quiz_score") or 0)
        expected = tracker.get_slot("quiz_current_letter")

        detected = get_current_gesture()

        if not expected:
            dispatcher.utter_message(text="Hmm, something went wrong. Say 'repeat' or 'test me' to restart.")
            return []

        if not detected:
            dispatcher.utter_message(text="Hmm, something went wrong. Say 'repeat' or 'test me' to restart.")
            return []

        if detected.upper() == expected.upper():
            score += 1
            dispatcher.utter_message(text="Yes! That's '{expected}'")
        else:
            dispatcher.utter_message(text=f"That's not right. Expected '{expected}' and saw '{detected}'.")

        index += 1

        if index >= len(quiz_letters):
            dispatcher.utter_message(text=f"All done! You got {score} out of {len(quiz_letters)}.")
            return [
                SlotSet("quiz_letters", []),
                SlotSet("quiz_current_letter", None),
                SlotSet("quiz_index", 0),
                SlotSet("quiz_score", 0)
            ]

        next_letter = quiz_letters[index]
        dispatcher.utter_message(text=f"Next, sign '{next_letter}'.")

        return [
            SlotSet("quiz_current_letter", next_letter),
            SlotSet("quiz_index", index),
            SlotSet("quiz_score", score)
        ]
        
class ActionRepeatQuizLetter(Action):
    def name(self):
        return "action_quiz_repeat_letter"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Repeat quiz letter.")
        current_letter = tracker.get_slot("quiz_current_letter")
        if current_letter:
            dispatcher.utter_message(text=f"Please sign '{current_letter}'.")
        else:
            dispatcher.utter_message(text="No quiz running. Say 'test me' to begin.")
        return []

class ActionQuizEnd(Action):
    def name(self):
        return "action_quiz_end"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Ending quiz.")
        score = tracker.get_slot("quiz_score") or 0
        index = tracker.get_slot("quiz_index") or 0

        if index == 0:
            dispatcher.utter_message(text="No quiz running.")
        else:
            dispatcher.utter_message(text=f"Quiz ended. You got {index} letter(s) with {score} correct.")

        return [
            SlotSet("quiz_letters", []),
            SlotSet("quiz_current_letter", None),
            SlotSet("quiz_score", 0),
            SlotSet("quiz_index", 0)
        ]

class ActionResetGesture(Action):
    def name(self):
        return "action_gesture_reset"

    def run(self, dispatcher, tracker, domain):
        try:
            response = requests.post("http://localhost:5000/gesture/reset")
            if response.status_code == 200:
                print("[RASA] Gesture reset successfully.")
            else:
                print("[RASA] Failed to reset gesture.")
        except Exception as e:
            print(f"[RASA] Error resetting gesture: {e}")

        return []