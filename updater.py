import datetime
from mimetypes import init
import os
import json
from socket import timeout
from downloader import SSL_CERT, documents_dir, courses, home_dir, downloadFile
from scraper import getTableData
from fileManager import isFolder
from checker import needsDownload

TIME_DISPLAY = '%Y-%m-%d %H:%M:%S'

def autoEnabled():
    with open('config.json', 'r') as f:
        data = json.load(f)
    if data['auto_update'] == 'off': return False
    return True

def getlastCheckDate():
    with open("config.json", 'r') as f:
        data = json.load(f)
    return datetime.datetime.strptime(data['last_check'], TIME_DISPLAY)

#convert DD-MM-YYYY to YYYY-MM-DD
def formatDate(dateString):
    unformatted =  datetime.datetime.strptime(dateString, '%d-%m-%Y %H:%M:%S')
    return datetime.datetime.strptime(datetime.datetime.strftime(unformatted, TIME_DISPLAY), TIME_DISPLAY)


def updateDate(): #epic rhyme
    now = {"last_check": datetime.datetime.strftime(datetime.datetime.now(), TIME_DISPLAY) }
    jsonData = now
    with open("config.json", 'r') as f:
        data = json.load(f)
    data.update(jsonData)
    with open("config.json", 'w') as jf:
        json.dump(data, jf)

def iterateAndDownload(last_check, courseId, url, session):
    print(f"\nSearching in {url}...")
    try:
        r = session.get(url, verify=SSL_CERT, timeout=5)
        with open("temp.html", 'w', encoding='utf8') as html:
            html.write(r.text)

        for data in getTableData("temp.html"): #iterate through each file in the table of contents 
            if isFolder(data['dl']):
                redir = f"{home_dir}{data['link']}"
                iterateAndDownload(last_check, courseId, redir, session) #go one level deeper  
            else:
                if formatDate(data['date']) >= last_check:
                    print(f"Update found for {data['file']}")
                    downloadFile(data['dl'], data['file'], courseId, session)
    except Exception as e: print(f"Request timeout! \n-------\n{e}\n-------\n{url} likely is a link and not a file.")

def scanCoursesForUpdates(session, courseId, specificCourse = None):
    last_check = getlastCheckDate()
    updateDate()

    if specificCourse == None:
        years = ["year_a", "year_b", "year_c", "year_d"]
        for year in years:
            for course in courses[year]:
                if not needsDownload(course, session):
                    cId = courses[year][course]
                    initial_url = f"{documents_dir}{cId}"
                    print(f"----\nScanning {cId} for updates...\n----")
                    iterateAndDownload(last_check, courses[year][course], initial_url, session)
                    print(f"\n{cId} is now up-to-date!\n")
    else:
        cId = courseId
        initial_url = f"{documents_dir}{cId}"
        print(f"Scanning {cId} for updates...")
        iterateAndDownload(last_check, specificCourse, initial_url, session)
        print(f"\n{cId} is now up-to-date!")

    print("Finished")
    if os.path.exists('temp.html'): os.remove('temp.html')
   
def determineAutoUpdate(session):
    lastCheck = getlastCheckDate()
    now = datetime.datetime.now()
    time_passed = abs((now - lastCheck).days)
    if time_passed >= 1:
        print(f"Some time has passed since the last update, auto-updating now!")
        scanCoursesForUpdates(session, '')
