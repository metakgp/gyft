from requests import Session
from utils.data import Endpoints


def get_cookies(session: Session, timetable_details):
    # This is just a hack to get cookies. TODO: do the standard thing here
    abc = session.post(Endpoints.ERP_TIMETABLE_URL, headers=headers, data=timetable_details)
    cookie_val = None
    for a in session.cookies:
        if (a.path == "/Acad/"):
            cookie_val = a.value

    cookie = {
        'JSESSIONID': cookie_val,
    }
    return cookie
