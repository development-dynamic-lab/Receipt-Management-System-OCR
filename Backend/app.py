import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
import requests

# Load environment variables from .env file
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Get the absolute path for frontend directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Backend directory
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../Frontend"))

# Initialize Flask app with absolute template and static folder paths
app = Flask(__name__, template_folder=os.path.join(FRONTEND_DIR, "templates"), 
            static_folder=os.path.join(FRONTEND_DIR, "static"))

# Load Firebase credentials and initialize Firebase Admin SDK
cred_path = os.path.join(FRONTEND_DIR, "firebase", "receipt-ocr-27b54-firebase-adminsdk-fbsvc-be8e44e115.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)


@app.route('/')
def home():
    """Render the login page."""
    return render_template('html/login.html')


@app.route('/signup')
def signup():
    """Render the signup page."""
    return render_template('html/signup.html')


@app.route('/dashboard')
def dashboard():
    """Render the user dashboard page."""
    return render_template('html/dashboard.html')


@app.route('/api/sendlogincredentials', methods=['POST'])
def getcredentials():
    """Authenticate user credentials using Firebase Authentication API."""
    data = request.get_json()
    email = data.get('username')
    password = data.get('password')

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(firebase_auth_url, json=payload)
        result = response.json()
        user_uuid = result.get('localId')

        if 'idToken' in result:
            return jsonify({"username": email, "status": "Login successful", "user_uuid": user_uuid})
        else:
            return jsonify({"error": result.get('error', {}).get('message', 'Login failed')}), 401

    except Exception as e:
        return jsonify({"error": "An error occurred during login"}), 500



@app.route('/api/sendcredentialstofirebase', methods=['POST'])
def setcredentials():
    """Register a new user in Firebase Authentication."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"email": email, "status": "Signup successful"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
