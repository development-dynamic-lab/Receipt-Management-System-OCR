##Imports
import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
from AI_OCR.modules.responses import ResponseAnalysis
from AI_OCR.gemini import GeminiOCR

# Load environment variables
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Get absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../Database"))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../Frontend"))

# Initialize Flask app with custom template/static folders
app = Flask(__name__, 
            template_folder=os.path.join(FRONTEND_DIR, "templates"),
            static_folder=os.path.join(FRONTEND_DIR, "static"))

# Load Firebase credentials and initialize Firebase Admin SDK
cred_path = os.path.join(DATABASE_DIR, "firebase", "receipt-ocr-27b54-firebase-adminsdk-fbsvc-be8e44e115.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Set uploads folder path
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ ROUTES ------------------ #

@app.route('/')
def home():
    # Render login page
    return render_template('html/login.html')

@app.route('/signup')
def signup():
    # Render signup page
    return render_template('html/signup.html')

@app.route('/dashboard')
def dashboard():
    # Render dashboard page
    return render_template('html/dashboard.html')

@app.route('/api/sendlogincredentials', methods=['POST'])
def getcredentials():
    # Authenticate user with Firebase Authentication API
    data = request.get_json()
    personName = data.get('personName')
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
            return jsonify({
                "loginName": personName,
                "username": email,
                "status": "Login successful",
                "user_uuid": user_uuid
            })
        else:
            return jsonify({"error": result.get('error', {}).get('message', 'Login failed')}), 401
    except Exception as e:
        return jsonify({"error": "An error occurred during login"}), 500

@app.route('/api/sendcredentialstofirebase', methods=['POST'])
def setcredentials():
    # Register a new user with Firebase Authentication
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

@app.route('/api/upload-images', methods=['POST'])
def upload_images():
    try:
        # Upload and process image files for OCR
        uploaded_files = os.listdir(UPLOAD_FOLDER)
        if len(uploaded_files) > 0:
            for file in uploaded_files:
                file_path = os.path.join(UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        if 'images' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('images')
        for file in files:
            if file.filename:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                
        if(len(os.listdir(UPLOAD_FOLDER))> 5):
            print("More than 5 images are passed for analysis")
            return jsonify({'status': 'failed'})
        
        all_analysis = image_analysis()
        print('All analysis: ',all_analysis)
        
        return jsonify({'status': 'success', 'all_analysis': all_analysis})
    except Exception as e:
        print(e)

def image_analysis():
    try:
        # Analyze uploaded images using Gemini OCR
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        gemini_ocr = GeminiOCR(api_key=gemini_api_key)

        receipts = os.listdir(UPLOAD_FOLDER)
        raw_analysis = []

        for receipt in receipts:
            receipt_path = os.path.join(UPLOAD_FOLDER, receipt)
            try:
                analysis_text = gemini_ocr.analyze_receipt(image_file=receipt_path)
            except Exception as e:
                analysis_text = f"wrong_image"
            raw_analysis.append(analysis_text)
            
        ##pre process the response 
        final_analysis = ResponseAnalysis(analysis_list = raw_analysis).get_analysed_response()
        return final_analysis

    except Exception as e:
        print(e)

def run_app():
    try:
      app.run(debug = True)
    except Exception as e:
        print(e)

# ------------------ RUN FLASK ------------------ #
if __name__ == "__main__":
    app.run(debug=True)
