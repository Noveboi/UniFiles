import datetime
import os
import json
from downloader import SSL_CERT, documents_dir, courses, home_dir, downloadFile
from scraper import getTableData
from fileManager import isFolder

TIME_DISPLAY = '%Y-%m-%d %H:%M:%S'

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

def iterateAndDownload(last_check, course, url, session):
    print(f"\nSearching in {url}...")

    r = session.get(url, verify=SSL_CERT)
    with open("temp.html", 'w') as html:
        html.write(r.text)

    for data in getTableData("temp.html"): #iterate through each file in the table of contents 
        if isFolder(data['dl']):
            redir = f"{home_dir}{data['link']}"
            iterateAndDownload(last_check, course, redir, session) #go one level deeper  
        else:
            if formatDate(data['date']) >= last_check:
                    print(f"Update found for {data['file']}")
                    downloadFile(data['dl'], data['file'], course, session)

def scanCoursesForUpdates(session, specificCourse = None):
    last_check = getlastCheckDate()
    updateDate()

    if specificCourse == None:
        for course in courses:
            cId = courses[course]
            initial_url = f"{documents_dir}{cId}"
            print(f"Scanning {cId} for updates...")
            iterateAndDownload(last_check, course, initial_url, session)
            print(f"\n{cId} is now up-to-date!")
    else:
        cId = courses[specificCourse]
        initial_url = f"{documents_dir}{cId}"
        print(f"Scanning {cId} for updates...")
        iterateAndDownload(last_check, specificCourse, initial_url, session)
        print(f"\n{cId} is now up-to-date!")

    print("Finished")
    os.remove('temp.html')
