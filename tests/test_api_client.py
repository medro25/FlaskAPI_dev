import unittest
from unittest.mock import patch, MagicMock
from services.api_client import LuxidAPIClient

class TestLuxidAPIClient(unittest.TestCase):

    def setUp(self):
        """Set up test instance."""
        self.client = LuxidAPIClient("test_user", "test_password")

    @patch("services.api_client.requests.post")
    def test_authenticate_success(self, mock_post):
        """Test successful authentication."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"token": "mocked_token"}

        token = self.client.authenticate()
        self.assertEqual(token, "mocked_token")
    
    @patch("services.api_client.requests.get")
    def test_fetch_events_success(self, mock_get):
        """Test fetching events successfully."""
        self.client.token = "mocked_token"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"event_id": "123"}]

        events = self.client.fetch_events()
        self.assertEqual(events, [{"event_id": "123"}])

    @patch("services.api_client.requests.get")
    def test_fetch_participants_success(self, mock_get):
        """Test fetching participants successfully."""
        self.client.token = "mocked_token"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"participant_id": "456"}

        participants = self.client.fetch_participants("https://api.example.com/events/123")
        self.assertEqual(participants, {"participant_id": "456"})

if __name__ == "__main__":
    unittest.main()
