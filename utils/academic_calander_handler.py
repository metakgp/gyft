from datetime import datetime
import os
import urllib.request


JSON_FOLDER_NAME = 'Academic_Cal-j'

#get the current working directory
def cwd():
    return os.getcwd()

#fetch the latest academic calendar from the iitkgp website
def get_latest_calendar():
    currYear = datetime.today().year
    currMonth = datetime.today().month

    if(currMonth < 7):
        currYear -= 1
    
    yearString = str(currYear) + '_' + str((currYear % 100) + 1)
    fileName = 'ACADEMIC_CALENDAR_' + yearString + '.pdf'
    url = 'https://www.iitkgp.ac.in/assets/pdf/' + fileName
    
    urllib.request.urlretrieve(url,fileName)


