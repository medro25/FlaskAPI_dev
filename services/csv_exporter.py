import csv
import os

class CSVExporter:
    def __init__(self, file_name="participants.csv"):
        # Ensure CSV is saved in the same directory as app.py
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_name = os.path.join(self.base_dir, file_name)
        print(f"  CSV will be saved at: {self.file_name}", flush=True)  # Debugging

    def save_to_csv(self, data):
        """Saves participant data to CSV."""
        if not data:
            print("No data to write to CSV.", flush=True)
            raise Exception("No data to write.")

        print("  Writing CSV file...", flush=True)

        fieldnames = [
            "eventId", "eventStartTime", "eventEndTime", "eventType",
            "firstName", "lastName", "emailAddress", "willAttend",
            "didAttend", "marketingConsent", "orderNewsletter"
        ]

        try:
            with open(self.file_name, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f" CSV file created successfully at {self.file_name}", flush=True)
            return f"CSV file has been successfully created."
        except Exception as e:
            print(f"Error writing CSV file: {str(e)}", flush=True)
            raise Exception(f"Error writing CSV file: {str(e)}")
