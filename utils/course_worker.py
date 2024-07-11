from dataclasses import dataclass, field
from requests import Response
from utils.dates import *
from typing import Dict
from iitkgp_erp_login import session_manager
from timetable import build_courses

@dataclass
class CourseWorker:

    sso_token: str = None
    sessionManager: session_manager.SessionManager = None
    roll_number: str = None
    jwt: str = None

    ERP_TIMETABLE_URL: str = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
    COURSES_URL: str = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm?semno={}&rollno={}"

    

    @classmethod
    def create_worker(cls, sessionManager: session_manager.SessionManager, roll_number , jwt) -> 'CourseWorker':
        _, ssoToken = sessionManager.get_erp_session(jwt=jwt)
        
        return cls( sso_token=ssoToken, roll_number=roll_number, sessionManager=sessionManager, jwt=jwt)

   

    def post(self, url: str, data=None, json=None) -> Response:
       
        return self.sessionManager.request(jwt=self.jwt, method="POST", url=url, data=data, json=json)


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
    
    def build_course(self)  :
        timetable_page = self.post(self.ERP_TIMETABLE_URL,
                                          data=self.get_timetable_details())
        course_names = self.get_course_names()
        courses= build_courses(timetable_page.text, course_names)

        return  courses


