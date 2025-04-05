# 🧾 Receipt Management System using OCR (with Gemini AI)

The **Receipt Management System** is a full-stack web application that allows users to **sign up, log in, and uploads receipts for analysis**. A key feature of this system is its integration with **Google's Gemini AI** for **Optical Character Recognition (OCR)** — enabling users to extract and manage receipt data efficiently from uploaded images.

The application is built using **Flask (Python)** for the backend and **Firebase Authentication** for secure user management. The **frontend** is developed using **HTML, CSS, and JavaScript**, and includes a clean UI for login, signup, and dashboard functionalities. The OCR component is implemented in the `gemini.py` script and uses Google's gemini-2.0 flash to analyze and extract text from receipt images.

---

## 📁 Project Structure

```
RECEIPT_OCR/
├── AI_OCR/              → gemini.py (OCR logic using Gemini AI)
├── Backend/             → Flask backend (flask_app.py)
├── Database/
│   ├── firebase/        → Firebase config & setup
│   └── PostgreSQL/      → PostgreSQL (optional for future)
├── Frontend/            → HTML templates and static assets
├── Images/              → Example receipt images or assets
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
🔐 Secure and modular backend architecture  

---

## ⚙️ Prerequisites

Make sure you have the following before getting started:

- Python 3.7 or above  
- Git installed on your system  
- Firebase API key (provided)  
- Google Gemini AI API key (you will generate this)  

---

## 🛠️ How to Set It Up (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:development-dynamic-lab/Receipt-Management-System-OCR.git
cd Receipt-Management-System-OCR
```

### 2️⃣ Create and Activate Virtual Environment

- **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

- **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and paste the following (with your actual keys):

```
FIREBASE_API_KEY=your_firebase_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```  
- You must generate your own **Google API key** from [Google AI Studio](https://aistudio.google.com/apikey) for OCR.

### 5️⃣ Run the Flask Application

```bash
python app.py
```

Once the server starts, open your browser and visit:  
🌐 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Test Credentials

Use this test user to try out the login feature:

**Email:** `anu@gmail.com`  
**Password:** `anu123`

Or register a new account using the signup page in the app.

---

## 📸 OCR Functionality (Gemini AI)

The `AI_OCR/gemini.py` file handles OCR by connecting with Google’s Gemini API. Users can upload receipt images via the dashboard, and the system will automatically extract and display the text content from the images using AI.

This feature is already integrated and fully functional — just make sure your Google API key is added to your `.env` file!

---

