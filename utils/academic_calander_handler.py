from datetime import datetime
import glob
import camelot
import os
import requests
import shutil
from zipfile import ZipFile

JSON_FOLDER_NAME = 'Academic_Cal-j'

#get the current working directory
def cwd():
    return os.getcwd()

def get_latest_calendar_name():
    curr_year = datetime.today().year
    curr_month = datetime.today().month

    if(curr_month < 7):
        curr_year -= 1
    
    year_str = str(curr_year) + '_' + str((curr_year % 100) + 1)
    filename = 'ACADEMIC_CALENDAR_' + year_str + '.pdf'
    return filename

def is_file_present(file):
    if(os.path.exists(cwd() + '/' + file)):
        return True
    return False

def delete_file(file):
    if(is_file_present(file)):
        try:
            print("DELETING file ",file)
            shutil.rmtree(cwd() + '/' + file)
        except Exception as e:
            print("ERROR: seems folder already exists but cannot be deleted")
            print(e)
            return False
    else:
        print("File not present..")

#fetch the latest academic calendar from the iitkgp website
def get_latest_calendar():
    
    filename = get_latest_calendar_name()
    filepath = cwd() + filename

    url = 'https://www.iitkgp.ac.in/assets/pdf/' + filename

    ## delete any old academic calander pdf if exists
    if(is_file_present(filename)):
        delete_file(filename)
   
    with open(filename,"wb") as file:
        response = requests.get(url)
        file.write(response.content)

    if(is_file_present(filename)):
        return True
    return False
    

