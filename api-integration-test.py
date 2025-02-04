import argparse
import requests
import erpcreds

BASE_URL = "http://127.0.0.1:8000"

session = requests.Session()

def get_secret_question():
    url = f"{BASE_URL}/secret-question"
    data = {"roll_number": erpcreds.ROLL_NUMBER}
    
    response = session.post(url, data=data)
    res_json = response.json()
    
    if res_json["status"] == "success":
        secret_question = res_json["SECRET_QUESTION"]
        session_token = res_json["SESSION_TOKEN"]
        print(f"✅ Session Token: {session_token}")
        return secret_question, session_token
    else:
        print(f"❌ Error: {res_json['message']}")
        exit(1)

def request_otp(session_token, secret_answer):
    url = f"{BASE_URL}/request-otp"
    headers = {"Session-Token": session_token}
    data = {
        "roll_number": erpcreds.ROLL_NUMBER,
        "password": erpcreds.PASSWORD,
        "secret_answer": secret_answer,
    }
    
    response = session.post(url, headers=headers, data=data)
    res_json = response.json()
    
    if res_json["status"] == "success":
        print("✅ OTP request successful. Check your email for the OTP.")
    else:
        print(f"❌ Error: {res_json['message']}")
        exit(1)

def login(session_token, secret_answer, otp):
    url = f"{BASE_URL}/login"
    headers = {"Session-Token": session_token}
    data = {
        "roll_number": erpcreds.ROLL_NUMBER,
        "password": erpcreds.PASSWORD,
        "secret_answer": secret_answer,
        "otp": otp,
    }
    
    response = session.post(url, headers=headers, data=data)
    res_json = response.json()
    
    if res_json["status"] == "success":
        sso_token = res_json["ssoToken"]
        print(f"✅ Login successful. SSO Token: {sso_token}")
        return sso_token
    else:
        print(f"❌ Error: {res_json['message']}")
        exit(1)

def download_timetable(sso_token):
    url = f"{BASE_URL}/timetable"
    headers = {"SSO-Token": sso_token}
    data = {"roll_number": erpcreds.ROLL_NUMBER}
    
    response = session.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        with open(f"{erpcreds.ROLL_NUMBER}-timetable.ics", "wb") as file:
            file.write(response.content)
        print(f"✅ Timetable downloaded successfully as {erpcreds.ROLL_NUMBER}-timetable.ics")
    else:
        print(f"❌ Error: {response.json().get('message', 'Unknown error')}")
        exit(1)

def _getOTP(OTP_CHECK_INTERVAL: float, session_token: str, log: bool = False):
    import time
    import base64
    from googleapiclient.discovery import build


    def getMailID(service):
        subject = "OTP for Sign In in ERP Portal of IIT Kharagpur"

        query = f"subject:{subject}"
        results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
        messages = results.get("messages", [])
        
        if messages:
            message = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
            return message["id"]
        
        return None

    def generate_token():
        """Generates token.json from credentials.json file with readonly access to mails."""
        import os
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow

        token_path = os.path.join(os.getcwd(), "token.json")
        credentials_path = os.path.join(os.getcwd(), "credentials.json")

        scopes = ["https://www.googleapis.com/auth/gmail.readonly"]

        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)

            if not os.path.exists(token_path):
                with open(token_path, "w") as token:
                    token.write(creds.to_json())

        return creds

    creds = generate_token()
    service = build("gmail", "v1", credentials=creds)
    
    latest_mail_id = getMailID(service)
    request_otp(session_token, secret_answer)
    if log: 
        print("⏱︎ Waiting for OTP ...")
    
    while True:
        if (mail_id := getMailID(service)) != latest_mail_id:
            break
        time.sleep(OTP_CHECK_INTERVAL)
    
    mail = service.users().messages().get(userId="me", id=mail_id).execute()
    if "body" in mail["payload"]:
        body_data = mail["payload"]["body"]["data"]
        decoded_body_data = base64.urlsafe_b64decode(body_data).decode("utf-8")
        otp = [part for part in decoded_body_data.split() if part.isdigit()][-1]

        return otp

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--otp",
        action="store_true",
        help="Automate OTP fetching",
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    secret_question, session_token = get_secret_question()
    secret_answer = erpcreds.SECURITY_QUESTIONS_ANSWERS[secret_question]

    args = _parse_args()
    if args.otp:
        otp = _getOTP(OTP_CHECK_INTERVAL=2, session_token=session_token, log=True)
    else:
        request_otp(session_token, secret_answer)
        otp = input("Enter OTP received via email: ").strip()

    sso_token = login(session_token, secret_answer, otp)
    
    download_timetable(sso_token)
