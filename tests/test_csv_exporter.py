import unittest
import os
from services.csv_exporter import CSVExporter

class TestCSVExporter(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.getcwd(), "test_participants.csv")  # Ensure absolute path inside Docker
        self.exporter = CSVExporter(self.filename)

    def tearDown(self):
        """Remove test file after tests."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_to_csv(self):
        """Test writing data to CSV file."""
        test_data = [
            {
                "eventId": "1",
                "eventStartTime": "01-01-2025 10:00:00",
                "eventEndTime": "01-01-2025 12:00:00",
                "eventType": "B2B",
                "firstName": "Alice",
                "lastName": "Smith",
                "emailAddress": "alice@example.com",
                "willAttend": True,
                "didAttend": False,
                "marketingConsent": True,
                "orderNewsletter": "Yes"
            }
        ]

        message = self.exporter.save_to_csv(test_data)

        print(f"📁 Checking file existence at: {self.filename}")
        print(f"🔎 Current Working Directory: {os.getcwd()}")

        self.assertTrue(os.path.exists(self.filename))
        self.assertEqual(message, "CSV file has been successfully created.")

if __name__ == "__main__":
    unittest.main()
