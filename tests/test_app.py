import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up Flask test client."""
        self.client = app.test_client()
        self.client.testing = True

    @patch("services.event_processor.EventProcessor.process_events")
    @patch("services.csv_exporter.CSVExporter.save_to_csv")
    def test_fetch_participant_info(self, mock_save_to_csv, mock_process_events):
        """Test GET /fetch-participant-info endpoint with mocked services."""
        mock_process_events.return_value = None
        mock_save_to_csv.return_value = "CSV successfully generated."

        response = self.client.get("/fetch-participant-info")

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "CSV successfully generated.")

if __name__ == "_main_":
    unittest.main()