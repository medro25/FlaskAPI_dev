import base64
import requests
import time
from cachetools import TTLCache

class LuxidAPIClient:
    API_BASE_URL = "https://recruiment-api-1069519412575.europe-west3.run.app"
    LOGIN_ENDPOINT = "/login"

    # ✅ Create an in-memory cache with a TTL (time-to-live) of 15 minutes
    cache = TTLCache(maxsize=1, ttl=900)  # 900 seconds = 15 minutes

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ensure_token()  # ✅ Ensure token exists on startup

    def authenticate(self):
        """Fetch a new Bearer token and store it in cache."""
        auth_str = f"{self.username}:{self.password}"
        auth_bytes = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {auth_bytes}"}

        try:
            print("🔵 Requesting new token...")
            response = requests.post(self.API_BASE_URL + self.LOGIN_ENDPOINT, headers=headers)
            response.raise_for_status()
            data = response.json()

            token = data.get("token")
            if not token:
                raise Exception("❌ Token missing in API response!")

            # ✅ Store the token and expiry time BEFORE accessing it
            self.cache["token"] = token
            self.cache["token_expiry"] = time.time() + 900  # ✅ Expiry = Now + 15 min

            # ✅ Print only after storing the token
            print(f"✅ New Token Stored: {token[:30]}... (Expires in 15 min)")
            return token
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication failed: {e}")
            raise Exception(f"Failed to authenticate: {e}")

    def ensure_token(self):
        """Ensure a valid token is available at startup."""
        try:
            token = self.cache["token"]
            token_expiry = self.cache["token_expiry"]
            if token_expiry < time.time():
                print("🔄 Token expired. Fetching a new one...")
                self.authenticate()
        except KeyError:
            print("🔄 No token found in cache. Authenticating...")
            self.authenticate()

    def get_headers(self):
        """Retrieve a valid token from cache or request a new one if expired."""
        try:
            token = self.cache["token"]
            token_expiry = self.cache["token_expiry"]

            if token_expiry < time.time():
                print("🔄 Token expired. Fetching a new one...")
                token = self.authenticate()
        except KeyError:  # ✅ Handle missing token
            print("🔄 Token missing. Authenticating...")
            token = self.authenticate()

        return {"Authorization": f"Bearer {token}"}

    def fetch_events(self):
        """Fetch events using a valid Bearer token."""
        headers = self.get_headers()
        try:
            print("🔵 Fetching events with headers:", headers)
            response = requests.get(f"{self.API_BASE_URL}/events", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch events: {e}")
            return None
