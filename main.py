import os
from datetime import datetime, timedelta

LOG_FILE = "visitors.txt"

# Exceptions expected by the tests
class DuplicateVisitorError(Exception):
    """Raised when a visitor is the same as the last visitor."""
    pass

class EarlyEntryError(Exception):
    """Raised when a visitor tries to log in before 5 minutes have passed."""
    pass

def ensure_file():
    """Ensure the log file exists."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            pass  # just create an empty file

def add_visitor(name):
    """
    Adds a visitor to the log file if:
    1. Not the same as the last visitor.
    2. At least 5 minutes have passed since the last visitor.

    Raises DuplicateVisitorError or EarlyEntryError as needed.
    Returns True if visitor logged successfully.
    """
    ensure_file()
    now = datetime.now()
    last_name = None
    last_time = None

    # Read last visitor and timestamp
    with open(LOG_FILE, "r") as f:
        lines = f.read().splitlines()
        if lines:
            last_entry = lines[-1]
            try:
                last_name, last_time_str = last_entry.split(" | ")
                last_time = datetime.fromisoformat(last_time_str)
            except ValueError:
                last_name = last_entry
                last_time = now - timedelta(minutes=10)  # assume enough time has passed

    # Check duplicate consecutive visitor
    if last_name == name:
        raise DuplicateVisitorError(f"Duplicate visitor '{name}' detected.")

    # Check 5-minute wait
    if last_time and (now - last_time) < timedelta(minutes=5):
        wait_seconds = int((timedelta(minutes=5) - (now - last_time)).total_seconds())
        raise EarlyEntryError(f"Please wait {wait_seconds} more seconds before logging a new visitor.")

    # Log visitor with timestamp
    with open(LOG_FILE, "a") as f:
        f.write(f"{name} | {now.isoformat()}\n")

    print(f"{name} logged successfully at {now.strftime('%H:%M:%S')}.")
    return True

# Optional manual testing loop
if __name__ == "__main__":
    print("Visitor logging ready!")
    while True:
        visitor = input("Enter visitor name (or 'exit' to quit): ").strip()
        if visitor.lower() == "exit":
            break
        try:
            add_visitor(visitor)
        except DuplicateVisitorError as e:
            print(e)
        except EarlyEntryError as e:
            print(e)
