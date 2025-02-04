import unittest
import os
from services.csv_exporter import CSVExporter

class TestCSVExporter(unittest.TestCase):

    def setUp(self):
        self.exporter = CSVExporter("test_participants.csv")

    def tearDown(self):
        """Remove test file after tests."""
        if os.path.exists("test_participants.csv"):
            os.remove("test_participants.csv")

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
        self.assertTrue(os.path.exists("test_participants.csv"))
        self.assertEqual(message, "test_participants.csv has been successfully created.")

if __name__ == "__main__":
    unittest.main()
