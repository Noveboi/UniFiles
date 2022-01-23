import requests
import datetime
import json
from downloader import SSL_CERT, documents_dir, yearA, home_dir, downloadFile, session
from scraper import getTableData
from fileManager import isFolder

### 
### DETECT IF FILE IS FOLDER, THEN GO IN IT AND SCAN ACCORDING FILES, FOLDERS DATES ARE NOT UP-TO-DATE
###

def getlastCheckDate():
    with open("config.json", 'r') as f:
        data = json.load(f)
    return datetime.date(datetime.datetime.strptime(data['last_check'], '%Y-%m-%d'))

def formatDate(dateString):
    #gunet's formatting: DD-MM-YYYY
    if dateString[0] == '0':
        day = int(dateString[1])
    else:
        day = int(dateString[0:2])

    if dateString[3] == '0':
        month = int(dateString[4])
    else:
        month = int(dateString[3:5])

    year = int(dateString[6:len(dateString)])
    return datetime.date(year, month, day)

def updateDate(): #epic rhyme
    now = {"last_check": datetime.datetime.now().date }#YYYY-MM-DD
    jsonData = json.dumps(now)
    with open("config.json", 'w') as f:
        f.write(jsonData)

def scanCoursesForUpdates():
    last_check = getlastCheckDate()
    updateDate()

    for course in yearA:
        cId = yearA[course]
        url = f"{documents_dir}{cId}"
        print(f"Scanning {cId} for updates...")
        r = session.get(url, verify=SSL_CERT)
        with open("temp.html", 'w') as html:
            html.write(r.text)
            
        for data in getTableData():
            if formatDate(data['date']) >= last_check:
                print(f"Update found for {data['file']}")
                downloadFile(data['dl'], data['file'], course)
