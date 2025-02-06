import base64
import requests
from cachetools import TTLCache
from config import USERNAME, PASSWORD

# In-memory cache for storing token
token_cache = TTLCache(maxsize=100, ttl=60 * 15)  # 15-minute expiry for debugging

class LuxidAPIClient:
    API_BASE_URL = "https://recruiment-api-1069519412575.europe-west3.run.app"
    LOGIN_ENDPOINT = "/login"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        """Fetches a new Bearer token and stores it in cache."""
        print("Requesting new token...", flush=True)
        auth_str = f"{self.username}:{self.password}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {auth_bytes}"}

        response = requests.post(self.API_BASE_URL + self.LOGIN_ENDPOINT, headers=headers)
        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                token_cache[self.username] = token  # Store token in cache
                print(f" Token Stored: {token} (Expires in 15 min)", flush=True)
            else:
                raise Exception("ERROR: Token was not stored in cache!")
        else:
            raise Exception(f"Authentication failed: {response.status_code}")

    def ensure_token(self):
        """Ensures a valid token is available before making API calls."""
        if self.username not in token_cache:
            print("No valid token found. Authenticating...", flush=True)
            self.authenticate()
        else:
            print(f" Using Token: {token_cache[self.username]} (Expires in {int(token_cache.ttl)}s)", flush=True)

    def get_headers(self):
        """Returns headers with authentication token."""
        print(f"Getting headers for {self.username}", flush=True)
        self.ensure_token()
        return {"Authorization": f"Bearer {token_cache[self.username]}"}

    def fetch_events(self):
        """Fetches event data from the API."""
        headers = self.get_headers()
        print(f"Fetching events with headers: {headers}", flush=True)

        response = requests.get(f"{self.API_BASE_URL}/events", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch events: {response.status_code}")
        
    def fetch_participants(self, participants_url):
        """Fetches participants from the given event URL."""
        headers = self.get_headers()
        print(f"Fetching participants from: {participants_url}", flush=True)

        response = requests.get(participants_url, headers=headers)
    
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch participants: {response.status_code}")

def get_api_client():
    """Helper function to initialize API client"""
    return LuxidAPIClient(USERNAME, PASSWORD)
