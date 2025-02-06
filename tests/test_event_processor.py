import unittest
from unittest.mock import MagicMock
from services.event_processor import EventProcessor

class TestEventProcessor(unittest.TestCase):

    def setUp(self):
        """Setup a mock API client and EventProcessor."""
        self.mock_api_client = MagicMock()
        self.processor = EventProcessor(self.mock_api_client)

    def test_format_datetime(self):
        """Test formatting of Unix timestamps into human-readable format."""
        formatted_time = self.processor.format_datetime(1736929800)
        self.assertEqual(formatted_time, "01-15-2025 08:30:00")  # UTC time conversion

    def test_extract_event_type_valid(self):
        """Test extraction of valid event types (b2b, b2c)."""
        custom_fields = {
            "3333": {"id": 3333, "title": "Event type", "value": {"22222": {"id": 22222, "value": "B2C"}}}
        }
        event_type = self.processor.extract_event_type(custom_fields)
        self.assertEqual(event_type, "b2c")  # Must be lowercase

    def test_extract_event_type_invalid(self):
        """Test handling of unexpected event types."""
        custom_fields = {
            "3333": {"id": 3333, "title": "Event type", "value": {"22222": {"id": 22222, "value": "Conference"}}}
        }
        event_type = self.processor.extract_event_type(custom_fields)
        self.assertEqual(event_type, "Invalid")  # Defaults to "Invalid"

    def test_process_participants_marketing_consent(self):
        """Test participant processing, ensuring marketing consent is correctly detected."""
        self.mock_api_client.fetch_participants.return_value = {
            "12345": {
                "answers": {
                    "firstname": {"answer": "John"},
                    "lastname": {"answer": "Doe"},
                    "email": {"answer": "john@example.com"},
                    "98765432": {"answer": {"1": {"choice": "Yes."}}}
                },
                "privacy_answers": [{"privacy_policy_id": 7295, "answer": 1}],  # Should set marketingConsent=True
                "will_attend": 1,
                "did_attend": 0
            }
        }

        self.processor.process_participants("event_1", "01-01-2025", "01-02-2025", "b2b", "https://mock-api.com")
        
        self.assertEqual(len(self.processor.all_participants), 1)
        participant = self.processor.all_participants[0]

        # Correct data extraction
        self.assertEqual(participant["firstName"], "John")
        self.assertEqual(participant["lastName"], "Doe")
        self.assertEqual(participant["emailAddress"], "john@example.com")

        # Will attend / Did attend
        self.assertTrue(participant["willAttend"])
        self.assertFalse(participant["didAttend"])

        # Marketing consent should be True
        self.assertTrue(participant["marketingConsent"])

    def test_process_participants_order_newsletter_multiple_conditions(self):
        """Test participant processing with Order Newsletter extracted from multiple conditions."""
        self.mock_api_client.fetch_participants.return_value = {
            "67890": {
                "answers": {
                    "firstname": {"answer": "Alice"},
                    "lastname": {"answer": "Smith"},
                    "email": {"answer": "alice@example.com"},
                    "98765432": {  # Known question ID
                        "answer": {
                            "1": {"choice": "Yes."}
                        }
                    }
                },
                "privacy_answers": [{"privacy_policy_id": 7295, "answer": 1}],
                "will_attend": 1,
                "did_attend": 1
            },
            "34567": {
                "answers": {
                    "firstname": {"answer": "Bob"},
                    "lastname": {"answer": "Johnson"},
                    "email": {"answer": "bob@example.com"},
                    "random_question": {  # Matching by "question": "Order newsletter"
                        "question": "Order newsletter",
                        "answer": {
                            "0": {"choice": "No."}
                        }
                    }
                },
                "privacy_answers": [{"privacy_policy_id": 7295, "answer": 1}],
                "will_attend": 1,
                "did_attend": 1
            }
        }

        self.processor.process_participants("event_5", "05-01-2025", "05-02-2025", "b2b", "https://mock-api.com")
        
        self.assertEqual(len(self.processor.all_participants), 2)
        
        # Alice's orderNewsletter should be "Yes."
        self.assertEqual(self.processor.all_participants[0]["orderNewsletter"], "Yes.")

        # Bob's orderNewsletter should be "No."
        self.assertEqual(self.processor.all_participants[1]["orderNewsletter"], "No.")

    def test_process_participants_missing_fields(self):
        """Test participant processing when some fields are missing."""
        self.mock_api_client.fetch_participants.return_value = {
            "54321": {
                "answers": {},  # ❌ Missing name, email, etc.
                "privacy_answers": [{"privacy_policy_id": 7295, "answer": 1}],  # Marketing consent still True
                "will_attend": None,
                "did_attend": None
            }
        }

        self.processor.process_participants("event_3", "03-01-2025", "03-02-2025", "b2b", "https://mock-api.com")
        
        self.assertEqual(len(self.processor.all_participants), 1)
        participant = self.processor.all_participants[0]

        # Default empty values for missing fields
        self.assertEqual(participant["firstName"], "")
        self.assertEqual(participant["lastName"], "")
        self.assertEqual(participant["emailAddress"], "")

        # Will attend / Did attend should default to False
        self.assertFalse(participant["willAttend"])
        self.assertFalse(participant["didAttend"])

        # Marketing consent should still be True
        self.assertTrue(participant["marketingConsent"])

    def test_process_participants_no_marketing_consent(self):
        """Test participant processing when marketing consent is not given."""
        self.mock_api_client.fetch_participants.return_value = {
            "67890": {
                "answers": {
                    "firstname": {"answer": "Alice"},
                    "lastname": {"answer": "Smith"},
                    "email": {"answer": "alice@example.com"},
                    "98765432": {"answer": {"1": {"choice": "No."}}}
                },
                "privacy_answers": [{"privacy_policy_id": 1015, "answer": 1}],  # ❌ No 7295
                "will_attend": 0,
                "did_attend": 1
            }
        }

        self.processor.process_participants("event_2", "02-01-2025", "02-02-2025", "b2c", "https://mock-api.com")
        
        self.assertEqual(len(self.processor.all_participants), 1)
        participant = self.processor.all_participants[0]

        # Will attend / Did attend
        self.assertFalse(participant["willAttend"])
        self.assertTrue(participant["didAttend"])

        # ❌ Marketing consent should be False
        self.assertFalse(participant["marketingConsent"])

if __name__ == "__main__":
    unittest.main()
