from flask import Flask, jsonify
from services.api_client import LuxidAPIClient
from config import USERNAME, PASSWORD

app = Flask(__name__)

# ✅ Initialize API client and ensure token is available
api_client = LuxidAPIClient(USERNAME, PASSWORD)
api_client.ensure_token()  # ✅ Ensure token exists on startup

@app.route("/fetch-participant-info", methods=["GET"])
def fetch_participant_info():
    try:
        print("🔵 Fetching participant info...", flush=True)

        # ✅ Ensure the token is valid before fetching data
        headers = api_client.get_headers()

        events = api_client.fetch_events()

        if events is None:
            return jsonify({"error": "Failed to fetch events"}), 500

        return jsonify({"events": events}), 200

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
