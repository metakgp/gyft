import requests
from flask import Flask, request, send_file, jsonify
import io
import jwt
from flask_cors import CORS
from datetime import datetime, timedelta
from timetable import build_courses, generate_ics
# from session_manager import SessionManager
from utils import ERPSession, CourseWorker
from iitkgp_erp_login import session_manager as sessionManager
import logging
import os



app = Flask(__name__)
CORS(app)

jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

session_manager = sessionManager.SessionManager(
    jwt_secret_key=jwt_secret_key, headers=headers)


class ErpResponse:
    def __init__(self, success: bool, message: str = None, data: dict = None, status_code: int = 200):
        self.success = success
        self.message = message
        self.data = data or {}
        self.status_code = status_code

        if not success:
            logging.error(f" {message}")

    def to_dict(self):
        response = {
            "status": "success" if self.success else "error",
            "message": self.message
        }
        if self.data:
            response.update(self.data)
        return response

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code


def handle_auth() -> ErpResponse:
    if "Authorization" in request.headers:
        header = request.headers["Authorization"].split(" ")
        if len(header) == 2:
            return ErpResponse(True, data={
                "jwt": header[1]
            }).to_response()
        else:
            return ErpResponse(False, "Poorly formatted authorization header. Should be of format 'Bearer <token>'", status_code=401).to_response()
    else:
        return ErpResponse(False, "Authentication token not provided", status_code=401).to_response()


@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form
        roll_number = data.get("roll_number")
        if not roll_number:
            return ErpResponse(False, "Roll Number not provided", status_code=400).to_response()

        secret_question, jwt = session_manager.get_secret_question(
            roll_number)
        return ErpResponse(True, data={
            "secret_question": secret_question,
            "jwt": jwt
        }).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        jwt = None
        auth_resp, status_code = handle_auth()
        if status_code != 200:
            return auth_resp, status_code
        else:
            jwt = auth_resp.get_json().get("jwt")

        password = request.form.get("password")
        secret_answer = request.form.get("secret_answer")
        if not all([password, secret_answer]):
            return ErpResponse(False, "Missing password or secret answer", status_code=400).to_response()

        session_manager.request_otp(jwt, password, secret_answer)
        return ErpResponse(True, message="OTP has been sent to your connected email accounts").to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/login", methods=["POST"])
def login():
    try:
        jwt = None
        auth_resp, status_code = handle_auth()
        if status_code != 200:
            return auth_resp, status_code
        else:
            jwt = auth_resp.get_json().get("jwt")

        password = request.form.get("password")
        secret_answer = request.form.get("secret_answer")
        otp = request.form.get("otp")
        if not all([secret_answer, password, otp]):
            return ErpResponse(False, "Missing password, secret answer or otp", status_code=400).to_response()

        session_manager.login(jwt, password, secret_answer, otp)
        return ErpResponse(True, message="Logged in to ERP").to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/logout", methods=["GET"])
def logout():
    try:
        jwt = None
        auth_resp, status_code = handle_auth()
        if status_code != 200:
            return auth_resp, status_code
        else:
            jwt = auth_resp.get_json().get("jwt")

        session_manager.end_session(jwt=jwt)

        return ErpResponse(True, message="Logged out of ERP").to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


    
@app.route("/download-ics", methods=["POST"])
def download_ics():
    try:
        jwt = None
        auth_resp, status_code = handle_auth()
        if status_code != 200:
            return auth_resp, status_code
        else:
            jwt = auth_resp.get_json().get("jwt")
        

        data = request.form
        roll_number = data.get("roll_number")
        
        couser_worker = CourseWorker.create_worker(sessionManager= session_manager, roll_number= roll_number,jwt= jwt)
        courses  = couser_worker.build_course()

        ics_content = generate_ics(courses, "")
        
        # Create an in-memory file-like object for the ics content
        ics_file = io.BytesIO()
        ics_file.write(ics_content.encode('utf-8'))
        ics_file.seek(0)

        return send_file(
            ics_file,
            as_attachment=True,
            mimetype='text/calendar',
            download_name=f"${roll_number}-timetable.ics"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the application on the local development server
    app.run()