# Luxid Flask Application 🚀  

This Flask-based application integrates with the **Luxid Recruitment API** to:  
- ✅ Authenticate using a **Bearer Token** (cached with TTL)  
- ✅ Fetch **event & participant details**  
- ✅ Process **hierarchical data** into a structured format  
- ✅ Export **participant data to a CSV file**  
- ✅ Run inside **Docker** for easy setup  

---

## 📌 **Table of Contents**  
- [🛠 Setup Instructions](#-setup-instructions)  
- [🚀 Running with Docker (Recommended)](#-running-with-docker-recommended)  
- [🧪 Running Tests](#-running-tests)  
- [🛠 Running Locally (Without Docker)](#-running-locally-without-docker)  
- [📌 Notes](#-notes)  
- [🎯 Contributing](#-contributing)  
- [📝 License](#-license)  

---

## 🛠 **Setup Instructions**  

Ensure you have the following installed:  
- **Python 3.10+** (if running locally)  
- **Docker & Docker Compose** (recommended for container execution)  
- **`pip`** (for local package installation)  

---

## 🚀 **Running with Docker (Recommended)**  

```sh
# 1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/luxid-flask-app.git
cd luxid-flask-app

# 2️⃣ Create a .env File
echo "LUXID_API_USERNAME=ApiUser1" > .env
echo "LUXID_API_PASSWORD=1jg91D101d1d01Md1" >> .env

# ⚠️ Do NOT commit the .env file to GitHub for security reasons!

# 3️⃣ Build & Run the Application
docker-compose up --build

# This will:
# 🔹 Build the Docker image
# 🔹 Start the Flask app container
# 🔹 Mount the local directory into /app inside the container

# The API will now be accessible at:
echo "API running at: http://localhost:5000/fetch-participant-info"

# 4️⃣ Fetch Participant Info
curl http://localhost:5000/fetch-participant-info

# This will:
# 🔹 Authenticate and fetch a Bearer Token
# 🔹 Retrieve event & participant data
# 🔹 Save processed data to participants.csv
# Luxid Flask Application 🚀  

This Flask-based application integrates with the **Luxid Recruitment API** to:  
- ✅ Authenticate using a **Bearer Token** (cached with TTL)  
- ✅ Fetch **event & participant details**  
- ✅ Process **hierarchical data** into a structured format  
- ✅ Export **participant data to a CSV file**  
- ✅ Run inside **Docker** for easy setup  

---

## 📌 **Table of Contents**  
- [🛠 Setup Instructions](#-setup-instructions)  
- [🚀 Running with Docker (Recommended)](#-running-with-docker-recommended)  
- [🧪 Running Tests](#-running-tests)  
- [🛠 Running Locally (Without Docker)](#-running-locally-without-docker)  
- [📌 Notes](#-notes)  
- [🎯 Contributing](#-contributing)  
- [📝 License](#-license)  

---

## 🛠 **Setup Instructions**  

Ensure you have the following installed:  
- **Python 3.10+** (if running locally)  
- **Docker & Docker Compose** (recommended for container execution)  
- **`pip`** (for local package installation)  

---

## 🚀 **Running with Docker (Recommended)**  

```sh
# 1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/luxid-flask-app.git
cd luxid-flask-app

# 2️⃣ Create a .env File
echo "LUXID_API_USERNAME=ApiUser1" > .env
echo "LUXID_API_PASSWORD=1jg91D101d1d01Md1" >> .env

# ⚠️ Do NOT commit the .env file to GitHub for security reasons!

# 3️⃣ Build & Run the Application
docker-compose up --build

# This will:
# 🔹 Build the Docker image  
# 🔹 Start the Flask app container  
# 🔹 Mount the local directory into `/app` inside the container  

# The API will now be accessible at:
echo "http://localhost:5000/fetch-participant-info"

# 4️⃣ Fetch Participant Info
curl http://localhost:5000/fetch-participant-info

# This will:
# 🔹 Authenticate and fetch a Bearer Token  
# 🔹 Retrieve event & participant data  
# 🔹 Save processed data to `participants.csv`

# 🔹 Running Tests Inside Docker  
docker exec -it flask-container sh -c "PYTHONPATH=/app pytest tests/"

# To run a specific test
docker exec -it flask-container sh -c "PYTHONPATH=/app pytest tests/test_event_processor.py -k test_extract_event_type_valid"
# 1️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 2️⃣ Install Dependencies
pip install -r requirements.txt

# 3️⃣ Run the Flask App
python app.py

# 4️⃣ Run Tests Locally
pytest tests/
