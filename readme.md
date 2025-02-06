# 🏆 Luxid Flask Application  

A **Flask-based API client** for the **Luxid API**, enabling:
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
- [🖥️ API Endpoint](#-api-endpoints)  
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


---

## 🚀 **Running with Docker (Recommended)**  

###  Clone the Repository  
```sh
https://github.com/medro25/FlaskApp_Luxid
```

###  Create a .env File  
```sh
echo "LUXID_API_USERNAME=your_username" > .env
echo "LUXID_API_PASSWORD=your_password" >> .env
```

###  Build & Run the Application  
```sh
docker-compose up
```


###  Access API  
```sh
 http://localhost:5000/fetch-participant-info
```

###  Stop & Remove Containers (when done)  
```sh
docker-compose down
```

---

## ⚙️ **Running Locally (Without Docker)**  

### 1️⃣ Clone Repository  
```sh
git clone https://github.com/YOUR_USERNAME/luxid-flask-app.git
cd luxid-flask-app
```

###  Create Virtual Environment  
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

###  Install Dependencies  
```sh
pip install -r requirements.txt
```

### Create a .env File (if not already created)  
```sh
echo "LUXID_API_USERNAME=your_username" > .env
echo "LUXID_API_PASSWORD=your_password" >> .env
```

###  Run Flask Application  
```sh
python app.py
```

### API will now be accessible at:  
```sh
"API running at: http://localhost:5000/fetch-participant-info"
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
```
