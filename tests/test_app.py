import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up Flask test client."""
        self.client = app.test_client()
        self.client.testing = True

    def test_fetch_participant_info(self):
        """Test GET /fetch-participant-info endpoint."""
        response = self.client.get("/fetch-participant-info")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

if __name__ == "__main__":
    unittest.main()
