import requests
from flask import Flask, request, send_file, jsonify
import io
import jwt
from flask_cors import CORS
from datetime import datetime, timedelta
from timetable import build_courses, generate_ics
from session_manager import SessionManager
from utils import ERPSession

app = Flask(__name__)
CORS(app, support_credentials=True)

# Initialize the SessionManager instance
session_manager = SessionManager()

@app.route("/create-session", methods=["POST"])
def create_session():
    try:
        data = request.form
        roll = data.get("roll")
        if not roll:
            return jsonify({"status": "error", "message": "Missing roll number"}), 400
        
        token = session_manager.create_session(roll)
        return jsonify({"status": "success", "token": token}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"status": "error", "message": "Missing token"}), 400
        
        secret_question = session_manager.get_secret_question(token)
        return jsonify({"status": "success", "secret_question": secret_question}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        token = request.headers.get("Authorization")
        passw = request.form.get("pass")
        secret_answer = request.form.get("secret_answer")
        
        if not all([token, passw, secret_answer]):
            return jsonify({"status": "error", "message": "Missing token, password, or secret answer"}), 400
        
        session_manager.request_otp(token, passw, secret_answer)
        return jsonify({"status": "success", "message": "OTP sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/login", methods=["POST"])
def login_and_download_ics():
    try:
        token = request.headers.get("Authorization")
        email_otp = request.form.get("email_otp")
        
        if not all([token, email_otp]):
            return jsonify({"status": "error", "message": "Missing token or email OTP"}), 400
        
        session_manager.establish_erp_session(token, email_otp)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/download-ics", methods=["POST"])
def download_ics():
    try:
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"status": "error", "message": "Missing token"}), 400
        
        session = session_manager.get_erp_session(token)
        erp_session = ERPSession.create_erp_session(session.requests_session, session.sso_token, session.login_details.get("user_id"))
        
        timetable_page = erp_session.post(erp_session.ERP_TIMETABLE_URL, cookies=True,
                                          data=erp_session.get_timetable_details())
        course_names = erp_session.get_course_names()
        courses = build_courses(timetable_page.text, course_names)

        ics_content = generate_ics(courses, "")
        
        # Create an in-memory file-like object for the ics content
        ics_file = io.BytesIO()
        ics_file.write(ics_content.encode('utf-8'))
        ics_file.seek(0)

        return send_file(
            ics_file,
            as_attachment=True,
            mimetype='text/calendar',
            download_name=f"{token}_timetable.ics"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the application on the local development server
    app.run()