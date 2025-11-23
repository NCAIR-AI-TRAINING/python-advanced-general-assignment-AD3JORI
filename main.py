import os
from datetime import datetime, timedelta

LOG_FILE = "visitors.txt"

def log_visitor(name):
    now = datetime.now()
    last_name = None

    # Read last visitor
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.read().splitlines()
            if lines:
                last_entry = lines[-1]
                try:
                    last_name, _ = last_entry.split(" | ")
                except ValueError:
                    last_name = last_entry

    # Check duplicate
    if last_name == name:
        print(f"Duplicate visitor '{name}' detected. Not logged.")
        return False

    def log_visitor(name):
        now = datetime.now()
        last_name = None
        last_time = None

        # Read last visitor and timestamp
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                lines = f.read().splitlines()
                if lines:
                    last_entry = lines[-1]
                    try:
                        last_name, last_time_str = last_entry.split(" | ")
                        last_time = datetime.fromisoformat(last_time_str)
                    except ValueError:
                        last_name = last_entry
                        last_time = now - timedelta(minutes=10)

        # Check duplicate
        if last_name == name:
            print(f"Duplicate visitor '{name}' detected. Not logged.")
            return False

        # Check 5-minute wait
        if last_time and now - last_time < timedelta(minutes=5):
            wait_seconds = int((timedelta(minutes=5) - (now - last_time)).total_seconds())
            print(f"Please wait {wait_seconds} more seconds before logging a new visitor.")
            return False

        # Log visitor with timestamp
        with open(LOG_FILE, "a") as f:
            f.write(f"{name} | {now.isoformat()}\n")
        print(f"{name} logged successfully at {now.strftime('%H:%M:%S')}.")
        return True

