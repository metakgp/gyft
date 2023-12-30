import requests
from requests import Session
from dataclasses import dataclass, field
from requests import Response
import iitkgp_erp_login.erp as erp
from types import MappingProxyType
from utils.dates import *
from typing import Dict


@dataclass
class ERPSession:
    session: Session
    session_token: str = None
    sso_token: str = None
    cookie: dict = None
    headers: Dict[str, str] = field(default_factory=lambda: {
        'timeout': '20',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
    })
    roll_number: str = None
    ERP_TIMETABLE_URL: str = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
    COURSES_URL: str = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm?semno={}&rollno={}"

    @classmethod
    def login(cls):
        r"""
        Logs into ERP using `iitkgp_erp_login` and returns an ERPSession object
        """
        erp_session = cls(session=requests.Session())
        erp_session.session_token, erp_session.sso_token = erp.login(erp_session.headers, erp_session.session)
        erp_session.roll_number = erp.ROLL_NUMBER
        erp_session.refresh_cookies()
        return erp_session

    def check_login(self) -> bool:
        r"""
        Checks if proper tokens and cookies exist
        """
        return self.sso_token is not None and self.cookie is not None and self.session is not None

    def post(self, url: str, data=None, json=None, cookies=None) -> Response:
        """
        Wrapper for post
        Args:
            url: URL for post request
            data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request
            json: (optional) json to send in the body of the Request.
            cookies: (optional) set to True to use stored cookies.

        Returns: Response
        """
        if cookies is True:
            cookies = self.cookie
        return self.session.post(url=url, data=data, json=json, headers=self.headers, cookies=cookies)

    def refresh_cookies(self) -> dict[str, str]:
        r"""
            Refreshes cookies and returns them for further use
        """
        # This is just a hack to get cookies. TODO: do the standard thing here
        timetable_details = self.get_timetable_details()
        self.post(self.ERP_TIMETABLE_URL, data=timetable_details)
        cookie_val = None
        for a in self.session.cookies:
            if a.path == "/Acad/":
                cookie_val = a.value

        cookie = {
            'JSESSIONID': cookie_val,
        }
        self.cookie = cookie
        return cookie

    # Ported code, in a function to be reused
    def get_timetable_details(self) -> dict[str, str]:
        return {
            "ssoToken": self.sso_token,
            "module_id": '16',
            "menu_id": '40',
        }
    
    def get_sem_num(self) -> int:
        if SEM_BEGIN.month > 6:
            # autumn semester
            return (int(SEM_BEGIN.strftime("%y")) - int(self.roll_number[:2])) * 2 + 1
        else:
            # spring semester - sem begin year is 1 more than autumn sem
            return (int(SEM_BEGIN.strftime("%y")) - int(self.roll_number[:2])) * 2 

    def get_course_page_details(self) -> dict[str, str]:
        return {
            "ssoToken": self.sso_token,
            "semno": self.get_sem_num(),
            "rollno": self.roll_number,
            "order": "asc"
        }

    def get_course_names(self) -> dict[str, str]:
        r"""
            Returns a mapping of course codes to course names
        """
        r = self.post(self.COURSES_URL.format(self.get_sem_num(), self.roll_number), data=self.get_course_page_details())
        sub_dict = {item["subno"]: item["subname"] for item in r.json()}
        return {k: v.replace("&amp;", "&") for k, v in sub_dict.items()}
