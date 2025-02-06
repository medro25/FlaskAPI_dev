import os
from flask import Flask, jsonify, send_file
from services.api_client import LuxidAPIClient
from services.event_processor import EventProcessor
from services.csv_exporter import CSVExporter
from config import USERNAME, PASSWORD

app = Flask(__name__)
api_client = LuxidAPIClient(USERNAME, PASSWORD)

# Define the file path where CSV will be stored inside the app directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(BASE_DIR, "participants.csv")
print(f"📂 CSV file will be saved in: {CSV_FILE_PATH}", flush=True)  # Debugging

@app.route("/fetch-participant-info", methods=["GET"])
def fetch_participant_info():
    """Endpoint to generate and save CSV file."""
    try:
        print("Fetching participant info...", flush=True)

        processor = EventProcessor(api_client)
        processor.process_events()

        # Generate CSV file in app directory
        exporter = CSVExporter(file_name=CSV_FILE_PATH)
        message = exporter.save_to_csv(processor.all_participants)

        return jsonify({
            "message": message,
            
        }), 200
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

@app.route("/download-csv", methods=["GET"])
def download_csv():
    """Endpoint to download the generated CSV file"""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return jsonify({"error": "CSV file not found!"}), 404

        return send_file(CSV_FILE_PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
