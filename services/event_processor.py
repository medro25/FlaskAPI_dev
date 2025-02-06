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
        """Extracts event type from nested structure and ensures valid values (b2b or b2c)."""
        valid_event_types = {"b2b", "b2c"}  # Accepted values
        default_type = "Invalid"  # Default fallback

        event_type_data = custom_fields.get("3333", {}).get("value", {})
        if event_type_data:
            first_key = list(event_type_data.keys())[0]  # Extract first key dynamically
            event_type = event_type_data[first_key]["value"]

            # Ensure the event type is valid (case-insensitive match)
            if event_type.lower() in valid_event_types:
                return event_type.lower()  # Return lowercase ('b2b' or 'b2c')
            else:
                print(f"Unexpected event type: '{event_type}'. Defaulting to '{default_type}'.")
        
        return default_type  # Return default if missing or invalid

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

            print(f"Processing Event {event_id}, URL: {participants_url}", flush=True)

            if participants_url:
                self.process_participants(event_id, start_time, end_time, event_type, participants_url)
            else:
                print(f"  No participants URL for event {event_id}", flush=True)

    def process_participants(self, event_id, start_time, end_time, event_type, participants_url):
        """Processes participants for a specific event."""
        participants = self.api_client.fetch_participants(participants_url)

        for participant_id, participant_data in participants.items():
            first_name = participant_data["answers"].get("firstname", {}).get("answer", "")
            last_name = participant_data["answers"].get("lastname", {}).get("answer", "")
            email_address = participant_data["answers"].get("email", {}).get("answer", "")

            marketing_consent = any(
                privacy.get("privacy_policy_id") == 7295 and privacy.get("answer") == 1
                for privacy in participant_data.get("privacy_answers", [])
            )
            
            # Extract orderNewsletter from multiple conditions
            order_newsletter = ""
            for key, answer_data in participant_data.get("answers", {}).items():
                if (
                    key == "98765432"  # Matches known question ID
                    or answer_data.get("question") == "Order newsletter"  # Matches question text
                ):
                    answer_choices = answer_data.get("answer", {})
                    if isinstance(answer_choices, dict):  # Ensure it's a dict
                        first_key = next(iter(answer_choices), None)
                        if first_key:
                            order_newsletter = answer_choices[first_key].get("choice", "")

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

        print(f" Participants Processed: {len(self.all_participants)}", flush=True)
