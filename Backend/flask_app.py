import os
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from Database.MySQL import action  ##new
from Llama_Agent.main import run_agent  ##new
import firebase_admin
from firebase_admin import credentials, auth
from AI_OCR.modules.responses import ResponseAnalysis
from AI_OCR.gemini import GeminiOCR
import shutil
import threading
import time
from celery import Celery

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
app.secret_key = os.urandom(24)

## Initialize the limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]  # fallback for other routes
)

# Load Firebase credentials and initialize Firebase Admin SDK
cred_path = os.path.join(DATABASE_DIR, "firebase", "receipt-ocr-27b54-firebase-adminsdk-fbsvc-be8e44e115.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',  # Redis broker URL
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = make_celery(app)

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

@app.route('/agent')
def agent():
    # Render dashboard page
    return render_template('html/agent.html')

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
            # Store UUID in session
            session['user_uuid'] = user_uuid
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

@limiter.limit("5 per 1 minute")
@app.route('/api/upload-images', methods=['POST'])
def upload_images():
    try:
        user_uuid = session.get('user_uuid')
        print("New login:", user_uuid)
        if not user_uuid:
            return jsonify({'error': 'User not authenticated'}), 401

        UPLOAD_FOLDER = os.path.join(BASE_DIR, user_uuid)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Check if the folder pre-exists and clear them all
        uploaded_files = os.listdir(UPLOAD_FOLDER)
        if len(uploaded_files) > 0:
            for file in uploaded_files:
                file_path = os.path.join(UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        if 'images' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        MAX_IMAGE_SIZE = 5 * 1024 * 1024  ## not more than 5MB
        
        files = request.files.getlist('images')
        for file in files:
            if file.filename:
                file.seek(0, os.SEEK_END)  # Move to end to get size
                file_length = file.tell()
                file.seek(0)  # Reset pointer back to start
                
                if file_length > MAX_IMAGE_SIZE:
                    print("Image size exceeded", file_length)
                    return jsonify({'error': f'File {file.filename} exceeds 5MB size limit'}), 400
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

        if len(os.listdir(UPLOAD_FOLDER)) > 5:
            print("More than 5 images are passed for analysis")
            return jsonify({'status': 'failed'})
        
        all_analysis = image_analysis.apply_async(args=[UPLOAD_FOLDER])
        print('All analysis: ', all_analysis)
        
        # Wait for the Celery task to complete and get the result
        result = all_analysis.get()
        action.store_receipts_for_user(user_uuid=user_uuid, receipts=result) ##new
        
        # Delete the folder after getting the result from Celery
        delayed_delete(UPLOAD_FOLDER)

        return jsonify({'status': 'success', 'all_analysis': result})
    except Exception as e:
        print(e)

# Celery task to analyze images in the background
@celery.task
def image_analysis(UPLOAD_FOLDER):
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

        ## Preprocess the response 
        final_analysis = ResponseAnalysis(analysis_list=raw_analysis).get_analysed_response()
        return final_analysis

    except Exception as e:
        print(e)
        return str(e)

def delayed_delete(folder_path, delay=3):
    def delete():
        time.sleep(delay)
        try:
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder {folder_path}: {e}")
    threading.Thread(target=delete).start()

##llama agent 
@app.route('/api/get_ai_response',methods=['POST']) 
def text_response():
    try:
        user_uuid = session.get('user_uuid')
        if not user_uuid:
            return jsonify({'error': 'User not authenticated'}), 401
        data = request.get_json()
        user_input = data['user_input']
        print("User Input:",user_input)
    except Exception as e:
        return jsonify({'error': 'Error getting response'}), 401
    
    response = run_agent(user_uuid=user_uuid, user_query=user_input)
    print(response)
    return jsonify({'botResponse':response})


def run_app():
    try:
        app.run(debug=True)
    except Exception as e:
        print(e)

# ------------------ RUN FLASK ------------------ #
if __name__ == "__main__":
    app.run(debug=True)