import unittest
from services.event_processor import EventProcessor

class TestEventProcessor(unittest.TestCase):

    def setUp(self):
        """Mock API client."""
        self.mock_api_client = unittest.mock.MagicMock()
        self.processor = EventProcessor(self.mock_api_client)

    def test_format_datetime(self):
        """Test date formatting from timestamp."""
        formatted_time = self.processor.format_datetime(1736929800)
        self.assertEqual(formatted_time, "01-15-2025 08:30:00")

    def test_extract_event_type(self):
        """Test event type extraction."""
        custom_fields = {
            "3333": {"id": 3333, "title": "Event type", "value": {"22222": {"id": 22222, "value": "B2B"}}}
        }
        event_type = self.processor.extract_event_type(custom_fields)
        self.assertEqual(event_type, "B2B")

    def test_process_participants(self):
        """Test participant processing logic."""
        self.mock_api_client.fetch_participants.return_value = {
            "12345": {
                "answers": {
                    "firstname": {"answer": "John"},
                    "lastname": {"answer": "Doe"},
                    "email": {"answer": "john@example.com"},
                    "98765432": {"answer": {"1": {"choice": "Yes"}}}
                },
                "privacy_answers": [{"privacy_policy_id": 7295, "answer": 1}],
                "will_attend": 1,
                "did_attend": 0
            }
        }

        self.processor.process_participants("event_1", "01-01-2025", "01-02-2025", "B2B", "https://mock-api.com")
        self.assertEqual(len(self.processor.all_participants), 1)
        self.assertEqual(self.processor.all_participants[0]["firstName"], "John")

if __name__ == "__main__":
    unittest.main()
