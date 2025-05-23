import subprocess
import time
import threading
import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

# Set paths for Python executables. These will be used instead of activating the virtual environments.
TRACKING_PYTHON = os.path.abspath("venv_tracking/Scripts/python.exe")
RASA_PYTHON = os.path.abspath("venv_rasa/Scripts/python.exe")

# Define the processes to be run together.
processes = {
    "Hand Tracking": [TRACKING_PYTHON, "app/flask_app.py"],
    "Rasa Actions": [RASA_PYTHON, "-m", "rasa", "run", "actions"],
    "Rasa Server": [RASA_PYTHON, "-m", "rasa", "run", "--enable-api", "--cors", "'*'"],
}

subprocesses = {}

def stream_output(name, proc):
    for line in proc.stdout:
        print(f"[{name}] {line.strip()}")

for name, cmd in processes.items():
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        encoding='utf-8',  
        errors='ignore'
    )
    subprocesses[name] = proc
    threading.Thread(target=stream_output, args=(name, proc), daemon=True).start()

# Start the speech handler in a separate window
speech_cmd = f'start "Speech Handler" cmd.exe /k ""{RASA_PYTHON}" handlers/speech_handler.py"'
subprocess.Popen(speech_cmd, shell=True)

# Coordinate shutdown of all processes
try:
    while True:
        for name, proc in subprocesses.items():
            if proc.poll() is not None:  
                print(f"\n[{name}] exited unexpectedly. Shutting down processes...")
                for p in subprocesses.values():
                    p.terminate()
                sys.exit(1)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTerminating all processes...")
    for p in subprocesses.values():
        p.terminate()
    sys.exit(0)
