import csv

class CSVExporter:
    def __init__(self, file_name="participants.csv"):
        self.file_name = file_name

    def save_to_csv(self, data):
        """Saves participant data to CSV."""
        if not data:
            raise Exception("No data to write.")

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
            return f"{self.file_name} has been successfully created."
        except Exception as e:
            raise Exception(f"Error writing CSV file: {str(e)}")
