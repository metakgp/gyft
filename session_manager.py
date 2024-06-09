import iitkgp_erp_login.erp as erp
import requests
from utils import ERPSession
from typing import Dict
from datetime import datetime, timedelta
from threading import Timer
headers = {
   'timeout': '20',
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}



class Session:
    def __init__(self, session_token: str ="", sso_token: str ="", erp_session: ERPSession = None, login_details: Dict[str, str] = None):
        self.session_token = session_token
        self.sso_token = sso_token
        self.requests_session = requests.Session()
        self.erp_session = erp_session
        self.login_details = login_details
        self.timestamp = datetime.now() 


class SessionManager:
    sessions: Dict[str, Session] = {}

    @staticmethod
    def get_secret_question(roll):
        session = SessionManager.sessions.get(roll)
        if not session:
            session = Session()
            SessionManager.sessions[roll] = session
        
        session_token = erp.get_sessiontoken(session.requests_session)
        session.session_token = session_token
        secret_question = erp.get_secret_question(headers, session.requests_session, roll)
        return secret_question

    @staticmethod
    def request_otp(roll, passw, secret_answer):
        session = SessionManager.sessions.get(roll)
        if not session:
            raise ValueError(f"No session found for roll number {roll}")
        
        login_details = erp.get_login_details(roll, passw, secret_answer, session.session_token)
        session.login_details = login_details
        erp.request_otp(headers, session.requests_session, login_details)

    @staticmethod
    def establish_erp_session(roll, email_otp):
        session = SessionManager.sessions.get(roll)
        if not session or not session.login_details:
            raise ValueError(f"No login details found for roll number {roll}")
        
        session.login_details["email_otp"] = email_otp
        sso_token = erp.signin(headers, session.requests_session, session.login_details)
        session.sso_token = sso_token
        erp_session = ERPSession.create_erp_session(session.requests_session, sso_token, roll)
        session.erp_session = erp_session
        return erp_session
     
    @staticmethod
    def get_erp_session(roll):
        session = SessionManager.sessions.get(roll)
        if not session or not session.erp_session:
            raise ValueError(f"No ERP session found for roll number {roll}")
        
        return session.erp_session

    @staticmethod
    def end_session(roll):
        if roll in SessionManager.sessions:
            del SessionManager.sessions[roll]
        return "Session ended"
    
    @staticmethod
    def cleanup_sessions():
        now = datetime.now()
        expired_sessions = [roll for roll, session in SessionManager.sessions.items()
                            if now - session.timestamp > timedelta(minutes=5)]
        for roll in expired_sessions:
            del SessionManager.sessions[roll]
        # Schedule the next cleanup in 5 minutes
        Timer(300, SessionManager.cleanup_sessions).start()


