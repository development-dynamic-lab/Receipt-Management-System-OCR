
## 🧾 Receipt Management System using OCR 

### 📌 Project Overview  
This is the **frontend** for a **Receipt Management System**, where users can **sign up, log in, and submit service credentials**. The UI is built using **HTML, CSS, and JavaScript**, while the backend is handled with **Flask and Firebase Authentication** for user management. **OCR functionality is not yet integrated**.  

---

### 🚀 Features  
✅ **User Authentication:** Signup & Login with Firebase Authentication 🔑  
✅ **Dashboard:** Navigate after login 📊  
✅ **Service Credential Submission:** Securely store user information 🔒  
✅ **Responsive UI:** Built with HTML, CSS, and JavaScript 🎨  

---

### 🛠️ Tech Stack  
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Database/Auth:** Firebase Authentication  

---

### 🏃‍♂️ How to Run the Project  

1. **Clone the repository (Using SSH):**  
   ```bash
   git clone git@github.com:development-dynamic-lab/Receipt-Management-System-OCR.git
   cd Receipt-Management-System-OCR
   ```  

2. **Create a virtual environment:**  
   ```bash
   python -m venv venv
   ```  

3. **Activate the virtual environment:**  
   - On **Windows** (Command Prompt):  
     ```bash
     venv\Scripts\activate
     ```  
   - On **Mac/Linux**:  
     ```bash
     source venv/bin/activate
     ```  

4. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```  

5. **Run the Flask server:**  
   ```bash
   python app.py
   ```  

6. **Access the application in your browser:**  
   ```
   http://127.0.0.1:5000/
   ```

---

### 🔑 Test Login Credentials  
Use the following test user for login:  
**Email:** `anu@gmail.com`  
**Password:** `anu123`  

Or, **signup a new user** through the UI.

---

### 📩 API Endpoints  
- **`POST /api/sendlogincredentials`** → Login authentication  
- **`POST /api/sendcredentialstofirebase`** → User registration  




