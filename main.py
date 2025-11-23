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

    # Log visitor (without 5-minute rule yet)
    with open(LOG_FILE, "a") as f:
        f.write(f"{name}\n")
    print(f"{name} logged successfully.")
    return True

# Testing loop
if __name__ == "__main__":
    print("Visitor logging ready!")
    while True:
        visitor = input("Enter visitor name (or 'exit' to quit): ").strip()
        if visitor.lower() == "exit":
            break
        log_visitor(visitor)
