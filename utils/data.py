from dataclasses import dataclass
from requests import Session


@dataclass
class ERPSession:
    session_token: str
    sso_token: str
    session: Session
    cookie: dict
    ERP_TIMETABLE_URL: str = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
    COURSES_URL: str = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm"

