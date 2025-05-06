import random
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop

# Get current gesture and emotion from Flask API
def get_current_tracking_state():
    try:
        response = requests.get("http://localhost:5000/tracking")
        data = response.json()
        return data.get("gesture"), data.get("emotion")
    except Exception as e:
        print(f"[RASA] Error fetching tracking state: {e}")
        return None, None

# Start the word quiz
class ActionWordQuizStart(Action):
    def name(self):
        return "action_word_quiz_start"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Starting word spelling quiz.")
        quiz_word = random.choice(["CAT", "DOG", "SUN", "CAR", "BUG"])
        quiz_letters = list(quiz_word)
        first_letter = quiz_letters[0]

        dispatcher.utter_message(text=f"Spell the word '{quiz_word}'.")
        dispatcher.utter_message(text=f"First, sign '{first_letter}'. Say 'I am ready' or 'Check me' when ready.")

        return [
            SlotSet("quiz_word", quiz_word),
            SlotSet("quiz_letters", quiz_letters),
            SlotSet("quiz_current_letter", first_letter),
            SlotSet("quiz_index", 0),
            SlotSet("quiz_score", 0),
            SlotSet("quiz_mode", "word")
        ]

# Check the letter and give feedback to user. Exit quiz when finished.
class ActionWordQuizCheckLetter(Action):
    def name(self):
        return "action_word_quiz_check_letter"

    def run(self, dispatcher, tracker, domain):
        print("[RASA] Checking spelling quiz letter.")
        quiz_letters = tracker.get_slot("quiz_letters") or []
        index = int(tracker.get_slot("quiz_index") or 0)
        score = int(tracker.get_slot("quiz_score") or 0)
        expected = tracker.get_slot("quiz_current_letter")

        detected_gesture, detected_emotion = get_current_tracking_state()

        if not expected or not detected_gesture:
            dispatcher.utter_message(text="Something went wrong. Say 'Start the word quiz' to begin again.")
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
            # Exit quiz and provide final score
            if score == 0:
                final_message = f"You didn't get any letters right, but it can only get better from here!"
            elif score < len(quiz_letters) / 2:
                final_message = f"You got {score}/{len(quiz_letters)}. Try again, you can do it!"
            elif score < len(quiz_letters):
                final_message = f"You got {score}/{len(quiz_letters)}. Try again, you are really close!"
            else:
                final_message = f"Perfect score! You got all the letters right. Amazing job!"

            dispatcher.utter_message(text=final_message)

            return [
                SlotSet("quiz_word", None),
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