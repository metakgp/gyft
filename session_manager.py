import iitkgp_erp_login.erp as erp
import requests
from utils import ERPSession

headers = {
   'timeout': '20',
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()


class SessionManager:
    rollTologinDetailsMap = {}
    rollToSessionTokenMap = {}

    @staticmethod
    def get_secret_question(roll):
        sessionToken = erp.get_sessiontoken(session)
        SessionManager.rollToSessionTokenMap[roll] = sessionToken
        secret_question = erp.get_secret_question(headers, session, roll)
        return secret_question
    
    @staticmethod
    def send_otp(roll, passw, secret_answer):
        sessionToken = SessionManager.rollToSessionTokenMap[roll]
        loginDetails = erp.get_login_details(roll, passw, secret_answer, sessionToken)
        SessionManager.rollTologinDetailsMap[roll] = loginDetails
        erp.request_otp(headers, session, loginDetails)

    
    @staticmethod
    def create_erp_session(roll, email_otp):
        loginDetails = SessionManager.rollTologinDetailsMap[roll]
        loginDetails["email_otp"] = email_otp
        ssoToken = erp.signin(headers, session, loginDetails)
        erp_session =  ERPSession.create_erp_session(session, ssoToken, roll)
        return erp_session
    
    @staticmethod
    def end_session(roll):
        SessionManager.rollTologinDetailsMap.pop(roll)
        SessionManager.rollToSessionTokenMap.pop(roll)
        return "Session ended"
    
