
# 🧾 Receipt Management System using OCR (with Gemini AI)

The **Receipt Management System** is a full-stack web application that allows users to **sign up, log in, and upload receipts for analysis**. A key feature of this system is its integration with **Google's Gemini AI** for **Optical Character Recognition (OCR)** — enabling users to extract and manage receipt data efficiently from uploaded images.

The application is built using **Flask (Python)** for the backend and **Firebase Authentication** for secure user management. The **frontend** is developed using **HTML, CSS, and JavaScript**, and includes a clean UI for login, signup, and dashboard functionalities. The OCR component is implemented in the `gemini.py` script and uses Google's Gemini 2.0 Flash model to analyze and extract text from receipt images.

---

## 📁 Project Structure

```
RECEIPT_OCR/
├── AI_OCR/              → gemini.py (OCR logic using Gemini AI)
├── Backend/             → Flask backend (flask_app.py)
├── Database/
│   ├── firebase/        → Firebase config & setup
│   └── MySQL/           → MySQL schema and logic (users, receipts, items)
├── Frontend/            → HTML templates and static assets
├── Images/              → Example receipt images or assets
├── Llama_Agent/         → AI agent logic using CrewAI and LLaMA3
├── visualPage/          → Static landing page (HTML/CSS/JS)
├── .env                 → Environment variables 
├── .gitignore
├── app.py               → Main app entry point
├── requirements.txt     → Python dependencies
└── README.md
```

---

## 🚀 Features

✅ User Signup & Login via Firebase

✅ Dashboard for submitting and managing credentials

✅ Google Gemini AI integration for OCR

✅ Image-to-Text extraction from uploaded receipts

✅ MySQL database integration to store structured data

✅ LLaMA3 AI agent (via Groq) for advanced automation

🔐 Secure and modular backend architecture

---

## ⚙️ Prerequisites

Make sure you have the following before getting started:

* Python 3.7 or above
* Git installed on your system
* Docker installed (for Redis)
* Firebase API key (provided)
* Google Gemini AI API key (you will generate this)
* MySQL server running locally or remotely
* Groq API key for LLaMA3 agent
* Internet access to use hosted LLM endpoints (Gemini, Groq)

---

## 🛠️ How to Set It Up (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:development-dynamic-lab/Receipt-Management-System-OCR.git
cd Receipt-Management-System-OCR
```

### 2️⃣ Create and Activate Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add:

```
FIREBASE_API_KEY=your_firebase_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# MySQL credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=receipt_db
```

---

### 5️⃣ Set Up MySQL Database

Use the following schema in MySQL:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_uuid VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    purchase_date DATE,
    store_name VARCHAR(255),
    total_amount DECIMAL(10, 2),
    consumption_tax DECIMAL(10, 2),
    payment_method VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id INT,
    english_name VARCHAR(255),
    quantity INT,
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);

ALTER TABLE receipts
ADD CONSTRAINT unique_receipt_entry
UNIQUE (user_id, purchase_date, store_name, total_amount);
```

---

### 6️⃣ Run Redis Server (Required for Celery Tasks)

```bash
docker run -d --name my-redis -p 6379:6379 redis
```

Or restart if already created:

```bash
docker restart my-redis
```

---

### 7️⃣ Start Celery Worker

```bash
celery -A Backend.flask_app.celery worker --loglevel=info --pool=solo
```

---

### 8️⃣ Start Flask App

```bash
python app.py
```

Visit your app at:
🌐 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Test Credentials

Use this test user to try out the login feature:

```
Email:    anu@gmail.com  
Password: anu123
```

Or register a new account using the signup page in the app.

---

## 📸 OCR Functionality (Gemini AI)

The `AI_OCR/gemini.py` file handles OCR by connecting with Google’s Gemini API. Users can upload receipt images via the dashboard, and the system will automatically extract and display the text content from the images using AI.

---

## 🤖 AI Agent (LLaMA 3 via CrewAI)

Inside the `Llama_Agent/` folder, the system includes a custom AI agent pipeline built using Groq API and Meta's LLaMA 3 70B model. This component performs intelligent receipt analysis tasks by interfacing directly with the Groq-hosted LLaMA3 model.

* Dynamically builds a prompt using `prompt_template.py`
* Sends the prompt to LLaMA 3 (70B) via Groq API `(groq_api.py)`
* Parses structured response (e.g., item names, prices, payment method)
* Extracts data intofrom MySQL via `db.py`

The model is served using **Groq API**, which allows ultra-fast inference and structured results.

You’ll need to provide your `GROQ_API_KEY` in `.env`.

---

## 📦 requirements.txt

```
# === Google Gemini Model ===
google
google-genai

# === Environment Variables ===
python-dotenv

# === Backend (Flask + Related) ===
flask
requests
Flask-Limiter
celery
redis

# === Firebase ===
firebase-admin

# === Database (MySQL) ===
mysql-connector-python

```

---

## 🎥 Demo

https://github.com/user-attachments/assets/e49c4e7f-bb92-4d01-a055-bf54c11fba21


