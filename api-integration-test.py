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
        print(f"✅ Secret Question: {secret_question}")
        print(f"✅ Session Token: {session_token}")
        return secret_question, session_token
    else:
        print(f"❌ Error: {res_json['message']}")
        exit(1)

def request_otp(session_token, secret_question):
    url = f"{BASE_URL}/request-otp"
    headers = {"Session-Token": session_token}
    data = {
        "roll_number": erpcreds.ROLL_NUMBER,
        "password": erpcreds.PASSWORD,
        "secret_answer": erpcreds.SECURITY_QUESTIONS_ANSWERS[secret_question],
    }
    
    response = session.post(url, headers=headers, data=data)
    res_json = response.json()
    
    if res_json["status"] == "success":
        print("✅ OTP request successful. Check your email for the OTP.")
    else:
        print(f"❌ Error: {res_json['message']}")
        exit(1)

def login(session_token, secret_question, otp):
    url = f"{BASE_URL}/login"
    headers = {"Session-Token": session_token}
    data = {
        "roll_number": erpcreds.ROLL_NUMBER,
        "password": erpcreds.PASSWORD,
        "secret_answer": erpcreds.SECURITY_QUESTIONS_ANSWERS[secret_question],
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

if __name__ == "__main__":
    secret_question, session_token = get_secret_question()
    request_otp(session_token, secret_question)
    
    otp = input("Enter OTP received via email: ").strip()
    sso_token = login(session_token, secret_question, otp)
    
    download_timetable(sso_token)
