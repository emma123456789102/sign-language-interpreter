import random
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop

def get_current_tracking_state():
    try:
        response = requests.get("http://localhost:5000/tracking")
        data = response.json()
        return data.get("gesture"), data.get("emotion")
    except Exception as e:
        print(f"[RASA] Error fetching tracking state: {e}")
        return None, None

class ActionLetterQuizStart(Action):
    def name(self):
        return "action_quiz_start"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Starting quiz.")
        quiz_letters = random.sample([chr(i) for i in range(65, 91)], 5)  # Generate 5 random letters A-Z
        first_letter = quiz_letters[0]

        dispatcher.utter_message(text="Let's get quizzy.")
        dispatcher.utter_message(text=f"First, sign '{first_letter}'. Say 'I am ready' or 'Check me' when ready.")

        return [
            SlotSet("quiz_letters", quiz_letters),
            SlotSet("quiz_current_letter", first_letter),
            SlotSet("quiz_index", 0),
            SlotSet("quiz_score", 0),
            SlotSet("quiz_mode", "letter")
        ]

class ActionLetterQuizCheckLetter(Action):
    def name(self):
        return "action_quiz_check_letter"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Checking quiz letter.")
        quiz_letters = tracker.get_slot("quiz_letters") or []
        index = int(tracker.get_slot("quiz_index") or 0)
        score = int(tracker.get_slot("quiz_score") or 0)
        expected = tracker.get_slot("quiz_current_letter")

        detected_gesture, detected_emotion = get_current_tracking_state()

        if not expected:
            dispatcher.utter_message(text="Hmm, something went wrong. Say 'Start the Alphabet Quiz' to restart.")
            return []

        if not detected_gesture:
            dispatcher.utter_message(text="Hmm, something went wrong. Say 'Start the Alphabet Quiz' to restart.")
            return []

        if detected_gesture.upper() == expected.upper():
            score += 1
            if detected_emotion == "happy":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Stay happy!")
            elif detected_emotion == "neutral":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Keep calm and carry on!")
            elif detected_emotion == "sad":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Don't be sad, you're doing great!")
            elif detected_emotion == "angry":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Don't be angry, you're doing well!")
            elif detected_emotion == "fear":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Don't worry, you're doing great!")
            elif detected_emotion == "disgust":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. Don't be upset, you're doing well!")
            elif detected_emotion == "surprise":
                dispatcher.utter_message(text=f"Correct! You got '{expected}'. I'm Surprised too. Keep it up!")
            else:
                dispatcher.utter_message(text=f"Correct! You got '{expected}'.")
        else:
            if detected_emotion == "happy":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. At least you're happy!")
            elif detected_emotion == "neutral":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Keep calm and carry on!")
            elif detected_emotion == "sad":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Don't be sad, have another go!")
            elif detected_emotion == "angry":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Don't be angry, keep trying!")
            elif detected_emotion == "fear":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Don't worry, have another go!")
            elif detected_emotion == "disgust":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Don't be upset, keep trying!")
            elif detected_emotion == "surprise":
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'. Surprised? Have another go!")
            else:
                dispatcher.utter_message(text=f"That's not right. I expected '{expected}' but you signed '{detected_gesture}'.")

        index += 1

        if index >= len(quiz_letters):
            dispatcher.utter_message(text=f"All done! You got {score} out of {len(quiz_letters)}.")
            return [
                SlotSet("quiz_letters", []),
                SlotSet("quiz_current_letter", None),
                SlotSet("quiz_index", 0),
                SlotSet("quiz_score", 0),
                SlotSet("quiz_mode", None)
            ]

        next_letter = quiz_letters[index]
        dispatcher.utter_message(text=f"Next, sign '{next_letter}'.")

        return [
            SlotSet("quiz_current_letter", next_letter),
            SlotSet("quiz_index", index),
            SlotSet("quiz_score", score)
        ]

class ActionLetterQuizRepeatLetter(Action):
    def name(self):
        return "action_quiz_repeat_letter"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Repeat quiz letter.")
        current_letter = tracker.get_slot("quiz_current_letter")
        if current_letter:
            dispatcher.utter_message(text=f"Try signing '{current_letter}'.")
        else:
            dispatcher.utter_message(text="No quiz running. Say 'Start the alphabet quiz' to begin.")
        return []

class ActionLetterQuizEnd(Action):
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