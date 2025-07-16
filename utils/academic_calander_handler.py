from datetime import datetime, timedelta
import glob
import camelot
import os
import requests
import shutil
from zipfile import ZipFile
import json
from dataclasses import dataclass
import re


JSON_FOLDER_NAME = 'Academic_Cal-j'

@dataclass
class DataEntry:
    start_date: datetime = datetime.today()
    end_date: datetime = datetime.today()
    event: str = ""

#get the current working directory
def cwd():
    return os.getcwd()

def get_latest_calendar_name():
    curr_year = datetime.today().year
    curr_month = datetime.today().month

    if(curr_month < 7):
        curr_year -= 1
    
    year_str = str(curr_year) + '-' + str((curr_year % 100) + 1)
    filename = 'AcademicCalendar' + year_str + '.pdf'
    return filename

def is_file_present(file):
    if(os.path.exists(cwd() + '/' + file) or
       os.path.exists(cwd() + '/' + file + '/')
       ):
        return True
    return False

def delete_file(file):
    if(is_file_present(file)):
        try:
            print("DELETING file ",file)
            if(os.path.isdir(file)):
                shutil.rmtree(cwd() + '/' + file)
            elif(os.path.isfile(file)):
                os.remove(file)
            else:
                raise Exception("filename not valid")
        except Exception as e:
            print("ERROR: seems file already exists but cannot be deleted")
            print(e)
            return False
    else:
        print(file, "File not present..")

#fetch the latest academic calendar from the iitkgp website
def get_latest_calendar():
    
    filename = get_latest_calendar_name()
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
    
def upzip_and_delete_zip(zip_file_name,result_folder_name):
    with ZipFile(zip_file_name) as zip:
        try:
            zip.extractall(result_folder_name)
        except Exception as E:
            print(E)
            return False

    print("Zip File not needed anymore, Deleteting ", zip_file_name)
    delete_file(zip_file_name)
    return True

def export_json():
    filename = get_latest_calendar_name()
    ## [NOTE]
    ## ignore the read_pdf not found warning
    ## also the devs of camelot have mismached backend names so ghostscript points to pdfium and vice versa ... 
    ## so basically this is using pdfium but backend name needs to be ghostscript
    ## in future if this gets fixed this need to be changed back
    tables = camelot.read_pdf(filename,pages="all",backend="ghostscript") 

    print("Checking for pre-existing folder")
    delete_file(JSON_FOLDER_NAME)

    try:
        tables.export((JSON_FOLDER_NAME + '.json'),f='json',compress=True)
    except Exception as E:
        print(E)
        return False

    upzip_and_delete_zip((JSON_FOLDER_NAME + '.zip'),JSON_FOLDER_NAME)
    return True

def get_json_files():
    folder_path = cwd() + '/' + JSON_FOLDER_NAME
    if(is_file_present(JSON_FOLDER_NAME)):
        files = glob.glob(folder_path + '/*.json',include_hidden=True)
        return files
    else:
        return []

def merge_json():
    merged_data = []
    for file in get_json_files():
        with open(file) as f:
            data = json.load(f)
            merged_data.extend(data)
    
    with open('final.json',"w") as f:
        json.dump(merged_data,f,indent=4)

    return merged_data

def get_academic_calendar() -> list[DataEntry]:

    get_latest_calendar()
    export_json()

    all_dates = merge_json()
    all_dates = all_dates[1:]

    main_dates = []
    # for date in all_dates:
    #     entry = DataEntry()
    #     if(len(date) > 4 and date['4'] != ''):
    #         if(len(date['1']) > 3):
    #             entry.event += date['1'].replace('\n','')
    #         entry.event += date['2'].replace('\n','')
    #         d = date['4'].replace('\n',' ').replace('(AN)','')
    #         print(d.find("to"))
    #         if(d.lower().find("to") != -1):
    #             d = str(d).lower().split("to")
    #             entry.start_date = datetime.strptime(d[0].split(" ")[0].strip(), "%d.%m.%Y")
    #             entry.end_date = datetime.strptime(d[-1].split(" ")[-1].strip(), "%d.%m.%Y")
    #         else:
    #             entry.start_date = datetime.strptime(d,"%d.%m.%Y")
    #             entry.end_date = ( entry.start_date + timedelta(1) )
    #     # elif(len(date) == 2 and date['1'] != ''):
    #     #     entry.event = date['0']
    #     #     d = date['1'].replace('\n','')
    #     #     if(d.find("to")):
    #     #         d = str(d).split("to")
    #     #         entry.start_date = datetime.strptime(d[0].strip(), "%A, %d %B %Y")
    #     #         entry.end_date = datetime.strptime(d[1].strip(), "%A, %d %B %Y")
    #     #     else:
    #     #         entry.start_date = datetime.strptime(d,"%A, %d %B %Y")
    #     #         entry.end_date = ( entry.start_date + timedelta(1) )
    #     # main_dates.append([date['0'],datetime_object])
    #     main_dates.append(entry)

    date_regex = re.compile(r'\d{2}.\d{2}.\d{4}')
    maxLen = 1
    for date in all_dates:
        if(len(date) > 4 and date['4'] != ''):
            entry = DataEntry()
            if(len(date['1']) > 3):
                entry.event += date['1'].replace('\n','')
            entry.event += date['2'].replace('\n','')

            d =date['3'].replace('\n',' ').replace('(AN)','') + date['4'].replace('\n',' ').replace('(AN)','')
            d = date_regex.findall(d)
            if(maxLen < len(d)):
                maxLen = len(d)
            if(len(d) == 1):
                entry.start_date = datetime.strptime(d[0],"%d.%m.%Y")
                entry.end_date = ( entry.start_date + timedelta(1) )
            elif(len(d) == 2):
                entry.start_date = datetime.strptime(d[0],"%d.%m.%Y")
                entry.end_date = datetime.strptime(d[1],"%d.%m.%Y")
            main_dates.append(entry)
        annual_convocation = str(date['1']).strip().lower().split(" ")
        ## KGP hai .. cannot trust, they can even mess up the spellings of annual convocation
        ## this can just reduce the amount of places this will fail
        if(len(annual_convocation) == 2 and ("annual" in annual_convocation or "convocation" in annual_convocation)):
            break

    return main_dates

