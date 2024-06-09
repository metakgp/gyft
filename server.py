import requests
# from flask import Flask
from flask import Flask, request,send_file,jsonify
from timetable import build_courses, generate_ics
import io

from flask_cors import CORS
from session_manager import SessionManager

app = Flask(__name__)
CORS(app, support_credentials=True)



@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form
        roll = data.get("roll")
        if not roll:
            return jsonify({"status": "error", "message": "Missing roll number"}), 400
        
        secret_question = SessionManager.get_secret_question(roll)
        return jsonify({"status": "success", "secret_question": secret_question}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        data = request.form
        roll = data.get("roll")
        passw = data.get("pass")
        secret_answer = data.get("secret_answer")
        
        if not all([roll, passw, secret_answer]):
            return jsonify({"status": "error", "message": "Missing roll number, password, or secret answer"}), 400
        
        SessionManager.request_otp(roll, passw, secret_answer)
        return jsonify({"status": "success", "message": "OTP sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/login", methods=["POST"])
def login_and_download_ics():
    try:
        data = request.form
        roll = data.get("roll")
        email_otp = data.get("email_otp")
        
        if not all([roll, email_otp]):
            return jsonify({"status": "error", "message": "Missing roll number or email OTP"}), 400
        
        SessionManager.establish_erp_session(roll, email_otp)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/download-ics", methods=["POST"])
def download_ics():
    try:
        data = request.form
        roll = data.get("roll")
        
        if not roll:
            return jsonify({"status": "error", "message": "Missing roll number"}), 400
        
        erp_session = SessionManager.get_erp_session(roll)
        
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
            download_name=f"{roll}_timetable.ics"
)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__': 
    # Run the application on the local development server 
    app.run()

