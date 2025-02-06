# 🏆 Luxid Flask Application  

A **Flask-based API client** for the **Luxid Recruitment API**, enabling:
- Authentication using **Bearer Token** (cached with TTL).
- Fetching **event & participant details**.
- Processing **hierarchical data** into a structured format.
- Exporting **participant data** to a CSV file.
- Running inside **Docker** for easy setup.

---

## 📑 **Table of Contents**  
- [🛠 Setup Instructions](#-setup-instructions)  
- [🚀 Running with Docker (Recommended)](#-running-with-docker-recommended)  
- [⚙️ Running Locally (Without Docker)](#-running-locally-without-docker)  
- [🧪 Running Tests](#-running-tests)  
- [🖥️ API Endpoints](#-api-endpoints)  
- [🐛 Debugging & Logs](#-debugging--logs)  
- [📌 Notes](#-notes)  

---

## 🛠 **Setup Instructions**  

### ✅ **Prerequisites**
Ensure you have installed:  
- **Python 3.10+** (if running locally)  
- **Docker & Docker Compose** (recommended for container execution)  
- **`pip`** (for package management)  

### 🌍 **API Access Requirements**
- You need **valid credentials** (`LUXID_API_USERNAME` and `LUXID_API_PASSWORD`) to authenticate.
- Ensure you **have an API key** or access rights from Luxid.

---

## 🚀 **Running with Docker (Recommended)**  

```sh
# 1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/luxid-flask-app.git
cd luxid-flask-app

# 2️⃣ Create a .env File
echo "LUXID_API_USERNAME=your_username" > .env
echo "LUXID_API_PASSWORD=your_password" >> .env

# 3️⃣ Build & Run the Application
docker-compose up --build -d  # Run in detached mode (background)

# 4️⃣ Check Running Containers
docker ps  # Shows running containers

# 5️⃣ Access API
curl http://localhost:5000/fetch-participant-info

# This will:
# ✅ Authenticate and fetch a Bearer Token
# ✅ Retrieve event & participant data
# ✅ Save processed data to participants.csv

# 6️⃣ Stop & Remove Containers (when done)
docker-compose down
```

---

## ⚙️ **Running Locally (Without Docker)**  

```sh
# 1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/luxid-flask-app.git
```
```sh
cd luxid-flask-app
```
# 2️⃣ Create Virtual Environment
```sh
python -m venv venv
```
```sh
source venv/bin/activate  # On Windows: 
```venv\Scripts\activate

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# 4️⃣ Create a .env File (if not already created)
echo "LUXID_API_USERNAME=your_username" > .env
echo "LUXID_API_PASSWORD=your_password" >> .env

# 5️⃣ Run Flask Application
python app.py

# API will now be accessible at:
echo "API running at: http://localhost:5000/fetch-participant-info"
```

---

## 🧪 **Running Tests**  

### ✅ Run Tests Locally  
```sh
pytest -v
```

### ✅ Run Tests in Docker  
```sh
docker-compose run --rm flask-app pytest -v
```

### ✅ Run Specific Test  
```sh
pytest tests/test_api_client.py -v