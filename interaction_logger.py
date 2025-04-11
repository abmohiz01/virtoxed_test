import json
import csv
from datetime import datetime
import os

class InteractionLogger:
    def __init__(self, format='json'):
        self.format = format.lower()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"interaction_log_{timestamp}.{self.format}"
        self.entries = []

        if self.format == 'csv':
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "browser", "url", "action", "details", "time_spent"])
                writer.writeheader()

    def log(self, browser, url, action, details=None, time_spent=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "browser": browser,
            "url": url,
            "action": action,
            "details": details,
            "time_spent": time_spent
        }

        if self.format == 'json':
            self.entries.append(entry)
            with open(self.filename, 'w') as f:
                json.dump(self.entries, f, indent=4)
        else:
            with open(self.filename, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=entry.keys())
                writer.writerow(entry)
