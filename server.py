import requests
# from flask import Flask
from flask import Flask, request, render_template , send_file   
import iitkgp_erp_login.erp as erp
from utils import ERPSession
from timetable import delete_calendar, create_calendar, build_courses, generate_ics
import io

from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)
session = requests.Session()
headers = {
   'timeout': '20',
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

dict = {
    'rollNo': 'sessionToken',
}


loginDetailsList = []

@app.route("/get_secret_question", methods=["POST"])

def get_secret_question():
    data = request.form
    roll = data.get("roll")
    print(roll)
    sessionToken = erp.get_sessiontoken(session)
    secret_question = erp.get_secret_question(headers, session, roll)
    dict[roll] = sessionToken
    return secret_question

@app.route("/sendOTP", methods=["POST"])
def login():
    data = request.form
    roll = data.get("roll")
    passw = data.get("pass")
    print(roll, passw)
    print(dict)
    sessionToken = dict[roll]
    secret_answer = data.get("secret_answer")
    loginDetails = erp.get_login_details(roll, passw, secret_answer, sessionToken)
    loginDetails["roll"] = roll
    loginDetailsList.append(loginDetails)
    erp.request_otp(headers, session, loginDetails)

    print(loginDetails)
    return "OTP sent"


@app.route("/verifyOTP", methods=["POST"])
def verifyOTP():
    data = request.form
    roll = data.get("roll")
    email_otp = data.get("email_otp")
    loginDetails = loginDetailsList[0]
    for i in loginDetailsList:
        if i["roll"] == roll:
            loginDetails = i
            break
    loginDetails["email_otp"] = email_otp
    ssoToken = erp.signin(headers, session, loginDetails)
    
    print(ssoToken)
   
    #send .ics file
    erp_session =  ERPSession.create_erp_session(session, ssoToken, roll)
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
    
    #remove loginDetails from list
    loginDetailsList.remove(loginDetails)
    # Return the ics file
    return send_file(ics_file, mimetype='text/calendar', as_attachment=True, download_name='timetable.ics')


if __name__ == '__main__': 
    # Run the application on the local development server 
    app.run()

