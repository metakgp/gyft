import requests
# from flask import Flask
from flask import Flask, request,send_file   
from timetable import build_courses, generate_ics
import io

from flask_cors import CORS
from session_manager import SessionManager

app = Flask(__name__)
CORS(app, support_credentials=True)



@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    data = request.form
    roll = data.get("roll")
    secret_question = SessionManager.get_secret_question(roll)
    return secret_question


@app.route("/send-otp", methods=["POST"])
def sendOTP():
    data = request.form
    roll = data.get("roll")
    passw = data.get("pass")
    secret_answer = data.get("secret_answer")
    
    SessionManager.send_otp(roll, passw, secret_answer)
    
    return "OTP sent"


@app.route("/verify-otp-and-download", methods=["POST"])
def verifyOTPAndDownloadICS():
    data = request.form
    roll = data.get("roll")
    email_otp = data.get("email_otp")
    
    erp_session =  SessionManager.create_erp_session(roll, email_otp)

    timetable_page = erp_session.post(erp_session.ERP_TIMETABLE_URL, cookies=True,
                                      data=erp_session.get_timetable_details())
    course_names = erp_session.get_course_names()
    courses = build_courses(timetable_page.text, course_names)

    print(f"Timetable fetched.\n")
    ics_content = generate_ics(courses, "")

    # Create an in-memory file-like object for the ics content
    ics_file = io.BytesIO()
    ics_file.write(ics_content.encode('utf-8'))
    ics_file.seek(0)  # Reset file pointer to the beginning
    
    SessionManager.end_session(roll)
    
    # Return the ics file
    return send_file(ics_file, mimetype='text/calendar', as_attachment=True, download_name='timetable.ics')


if __name__ == '__main__': 
    # Run the application on the local development server 
    app.run()

