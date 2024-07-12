import requests
from flask import Flask, request, send_file, jsonify
import io
from flask_cors import CORS
from timetable import build_courses, generate_ics
import logging
import iitkgp_erp_login.erp as erp
import iitkgp_erp_login.utils as erp_utils
from typing import Dict, List
from utils.dates import *


app = Flask(__name__)
CORS(app)

headers = {
    "timeout": "20",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def check_missing_fields(all_fields: Dict[str, str]) -> List[str]:
    return [field for field, value in all_fields.items() if not value]

class ErpResponse:
    def __init__(
        self,
        success: bool,
        message: str = None,
        data: dict = None,
        status_code: int = 200,
    ):
        self.success = success
        self.message = message
        self.data = data or {}
        self.status_code = status_code

        if not success:
            logging.error(f" {message}")

    def to_dict(self):
        response = {"status": "success" if self.success else "error"}
        if self.message:
            response["message"] = self.message
        if self.data:
            response |= self.data
        return response

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code




@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form
        all_fields = {
            "roll_number": data.get("roll_number"),
        }
        missing = check_missing_fields(all_fields)
        if len(missing) > 0:
            return ErpResponse(
                False, f"Missing Fields: {', '.join(missing)}", status_code=400
            ).to_response()

        session = requests.Session()
        secret_question = erp.get_secret_question(
            headers=headers,
            session=session,
            roll_number=all_fields["roll_number"],
            log=True,
        )
        sessionToken = erp_utils.get_cookie(session, "JSESSIONID")

        return ErpResponse(
            True,
            data={"SECRET_QUESTION": secret_question, "SESSION_TOKEN": sessionToken},
        ).to_response()
    except erp.ErpLoginError as e:
        return ErpResponse(False, str(e), status_code=401).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        data = request.form
        all_fields = {
            "roll_number": data.get("roll_number"),
            "password": data.get("password"),
            "secret_answer": data.get("secret_answer"),
            "sessionToken": request.headers["Session-Token"],
        }
        missing = check_missing_fields(all_fields)
        if len(missing) > 0:
            return ErpResponse(
                False, f"Missing Fields: {', '.join(missing)}", status_code=400
            ).to_response()

        login_details = erp.get_login_details(
            ROLL_NUMBER=all_fields["roll_number"],
            PASSWORD=all_fields["password"],
            secret_answer=all_fields["secret_answer"],
            sessionToken=all_fields["sessionToken"],
        )

        session = requests.Session()
        erp_utils.set_cookie(session, "JSESSIONID", all_fields["sessionToken"])
        erp.request_otp(
            headers=headers, session=session, login_details=login_details, log=True
        )

        return ErpResponse(
            True, message="OTP has been sent to your connected email accounts"
        ).to_response()
    except erp.ErpLoginError as e:
        return ErpResponse(False, str(e), status_code=401).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.form
        all_fields = {
            "roll_number": data.get("roll_number"),
            "password": data.get("password"),
            "secret_answer": data.get("secret_answer"),
            "otp": data.get("otp"),
            "sessionToken": request.headers["Session-Token"],
        }
        missing = check_missing_fields(all_fields)
        if len(missing) > 0:
            return ErpResponse(
                False, f"Missing Fields: {', '.join(missing)}", status_code=400
            ).to_response()

        login_details = erp.get_login_details(
            ROLL_NUMBER=all_fields["roll_number"],
            PASSWORD=all_fields["password"],
            secret_answer=all_fields["secret_answer"],
            sessionToken=all_fields["sessionToken"],
        )
        login_details["email_otp"] = all_fields["otp"]

        session = requests.Session()
        erp_utils.set_cookie(session, "JSESSIONID", all_fields["sessionToken"])
        ssoToken = erp.signin(
            headers=headers, session=session, login_details=login_details, log=True
        )

        return ErpResponse(True, data={"ssoToken": ssoToken}).to_response()
    except erp.ErpLoginError as e:
        return ErpResponse(False, str(e), status_code=401).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/timetable", methods=["POST"])
def download_ics():
    try:
        data = request.form
        all_fields = {
            "roll_number": data.get("roll_number"),
            "ssoToken": request.headers["SSO-Token"],
        }
        missing = check_missing_fields(all_fields)
        if len(missing) > 0:
            return ErpResponse(
                False, f"Missing Fields: {', '.join(missing)}", status_code=400
            ).to_response()
        
        roll_number = all_fields["roll_number"]
        ssoToken = all_fields["ssoToken"]

        ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
        COURSES_URL: str = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm?semno={}&rollno={}"

        
        session = requests.Session()
        erp_utils.populate_session_with_login_tokens(session, ssoToken)

        timetable_page = session.post(headers=headers, url=ERP_TIMETABLE_URL, data={
            "ssoToken": ssoToken,
            "module_id": '16',
            "menu_id": '40',
        })

        sem_num = 1
        
        if SEM_BEGIN.month > 6:
            # autumn semester
            sem_num = (int(SEM_BEGIN.strftime("%y")) - int(roll_number[:2])) * 2 + 1
        else:
            # spring semester - sem begin year is 1 more than autumn sem
            sem_num= (int(SEM_BEGIN.strftime("%y")) - int(roll_number[:2])) * 2


        
        r  = session.post(headers=headers, url=COURSES_URL.format(sem_num, roll_number), data={
            "ssoToken": ssoToken,
            "semno": sem_num,
            "rollno":   roll_number,
            "order": "asc"
        })



        sub_dict = {item["subno"]: item["subname"] for item in r.json()}
        course_names = {k: v.replace("&amp;", "&") for k, v in sub_dict.items()}
        
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
            download_name=f"${roll_number}-timetable.ics"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the application on the local development server
    app.run()