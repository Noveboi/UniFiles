import requests
import datetime
import os
import json
from downloader import SSL_CERT, documents_dir, yearA, home_dir, downloadFile, session
from scraper import getTableData
from fileManager import isFolder

### 
### DETECT IF FILE IS FOLDER, THEN GO IN IT AND SCAN ACCORDING FILES, FOLDERS DATES ARE NOT UP-TO-DATE
###

TIME_DISPLAY = '%Y-%m-%d %H:%M:%S'

def getlastCheckDate():
    with open("config.json", 'r') as f:
        data = json.load(f)
    return datetime.date(datetime.datetime.strptime(data['last_check'], '%Y-%m-%d'))

#convert DD-MM-YYYY to YYYY-MM-DD
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

def iterateAndDownload(last_check, course, url):
    print(f"\n----{url}----\n")
    
    r = session.get(url, verify=SSL_CERT)
    with open("temp.html", 'w') as html:
        html.write(r.text)

    for data in getTableData("temp.html"): #iterate through each file in the table of contents 
        if isFolder(data['dl']):
            redir = f"{home_dir}{data['link']}"
            iterateAndDownload(last_check, course, redir) #go one level deeper  
        else:
            if formatDate(data['date']) >= last_check:
                    print(f"Update found for {data['file']}")
                    downloadFile(data['dl'], data['file'], course)

def scanCoursesForUpdates():
    last_check = getlastCheckDate()
    updateDate()

    for course in yearA:
        cId = yearA[course]
        initial_url = f"{documents_dir}{cId}"
        print(f"Scanning {cId} for updates...")
            
        iterateAndDownload(last_check, course, initial_url)

cId = yearA['anal1']
last_check = datetime.date(2021,1,1)
url = f"{documents_dir}{cId}"
print(f"Scanning {cId} for updates...")
r = session.get(url, verify=SSL_CERT)
with open("temp.html", 'w') as html:
    html.write(r.text)

with open('downloads.json', 'w') as openFile:
    pass
    
iterateAndDownload(last_check, 'anal1', url)

os.remove('downloads.json')
os.remove('temp.html')