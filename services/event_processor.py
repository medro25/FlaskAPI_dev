from datetime import datetime

class EventProcessor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.all_participants = []

    @staticmethod
    def format_datetime(timestamp):
        """Converts Unix timestamp to formatted string."""
        return datetime.utcfromtimestamp(timestamp).strftime("%m-%d-%Y %H:%M:%S")

    def extract_event_type(self, custom_fields):
        """Extracts event type from nested structure."""
        event_type = "Unknown"
        event_type_data = custom_fields.get("3333", {}).get("value", {})
        if event_type_data:
            first_key = list(event_type_data.keys())[0]  # Extract first available key
            event_type = event_type_data[first_key]["value"]
        return event_type

    def process_events(self):
        """Processes events and their participants."""
        events = self.api_client.fetch_events()
        
        for event_item in events:
            event_id = list(event_item.keys())[0]
            event_data = event_item[event_id]

            start_time = self.format_datetime(event_data["start_time"])
            end_time = self.format_datetime(event_data["end_time"])
            event_type = self.extract_event_type(event_data.get("custom", {}))
            participants_url = event_data.get("participants_url")

            if participants_url:
                self.process_participants(event_id, start_time, end_time, event_type, participants_url)

    def process_participants(self, event_id, start_time, end_time, event_type, participants_url):
        """Processes participants for a specific event."""
        participants = self.api_client.fetch_participants(participants_url)

        for participant_id, participant_data in participants.items():
            first_name = participant_data["answers"].get("firstname", {}).get("answer", "")
            last_name = participant_data["answers"].get("lastname", {}).get("answer", "")
            email_address = participant_data["answers"].get("email", {}).get("answer", "")

            order_newsletter = ""
            newsletter_data = participant_data["answers"].get("98765432", {}).get("answer", {})
            if isinstance(newsletter_data, dict) and "1" in newsletter_data:
                order_newsletter = newsletter_data["1"].get("choice", "")

            # Extract marketing consent
            marketing_consent = False
            for privacy_entry in participant_data.get("privacy_answers", []):
                if privacy_entry.get("privacy_policy_id") == 7295:
                    marketing_consent = bool(privacy_entry.get("answer", 0))
                    break

            # Append structured data
            self.all_participants.append({
                "eventId": event_id,
                "eventStartTime": start_time,
                "eventEndTime": end_time,
                "eventType": event_type,
                "firstName": first_name,
                "lastName": last_name,
                "emailAddress": email_address,
                "willAttend": bool(participant_data.get("will_attend", False)),
                "didAttend": bool(participant_data.get("did_attend", False)),
                "marketingConsent": marketing_consent,
                "orderNewsletter": order_newsletter
            })
