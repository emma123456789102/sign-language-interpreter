import tkinter as tk
from tkinter import Label
import cv2
import requests
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

# 👇 Import the prediction function from the own module
from code.hand_tracking import predict_sign
# Communicate with Rasa chatbot
def get_rasa_response(user_message):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": user_message}
    try:
        response = requests.post(url, json=payload)
        messages = response.json()
        if messages:
            return messages[0].get("text", "")
    except Exception as e:
        print("Error talking to Rasa:", e)
    return ""

class SignLanguageApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Sign Language Chatbot")

        self.video_label = Label(window)
        self.video_label.pack()

        self.prediction_label = Label(window, text="Prediction: ", font=("Arial", 14))
        self.prediction_label.pack()

        self.rasa_response_label = Label(window, text="Rasa: ", font=("Arial", 14), fg="blue")
        self.rasa_response_label.pack()

        self.cap = cv2.VideoCapture(0)
        self.last_sign = ""
        self.update_video()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            sign = predict_sign(frame)
            if sign and sign != self.last_sign:
                self.last_sign = sign
                self.prediction_label.config(text=f"Prediction: {sign}")

                # Get response from Rasa
                response = get_rasa_response(sign)
                self.rasa_response_label.config(text=f"Rasa: {response}")

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.window.after(30, self.update_video)

    def close(self):
        self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
