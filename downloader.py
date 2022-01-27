import os
from bs4 import BeautifulSoup
from json import load
from scraper import getTableData, getCourseTitle
from fileManager import isFolder, modifyDirs, unzipAndOrganize, defineDownloadPath, local_dir
from checker import findYear

SSL_CERT = "cert/gunet2-cs-unipi-gr-chain.pem"  # certificate for SSL handshake
ENC = "utf8"

home_dir = "https://gunet2.cs.unipi.gr"
documents_dir = "https://gunet2.cs.unipi.gr/modules/document/document.php?course="
with open("courses.json", 'r') as jf:
    courses = load(jf)

def downloadFile(file_path,file_name,courseId,session):
    name = getCourseTitle(courseId, session)
    if '/' in name:
        name = name.replace('/', '|')
    local_subdir = os.path.join(local_dir, name)
    download_link = f"{home_dir}{file_path}" 
    try:
        d_r = session.get(download_link, verify=SSL_CERT)  # download request

        # store files in appropriate directory
        modifyDirs(local_subdir, file_name, download_link, d_r)

        # extract files from every .zip and put them in folders
        if isFolder(download_link):
            unzipAndOrganize(file_name, local_subdir)
    except Exception as e2:
        print(f"download request went wrong: {e2}")

def downloadSpecificCourse(courseKey,session, yearCourses):
    targetdocs_url = f"{documents_dir}{yearCourses[courseKey]}"
    try:
        # establish connection to website
        r = session.get(targetdocs_url, verify=SSL_CERT)

        # write to a temp dummy html file the websites contents
        with open("rawweb.html", "w", encoding=ENC) as f:
            f.write(BeautifulSoup(r.text, 'lxml').prettify())

        # assign appropriate link for GET download request
        for data in getTableData("rawweb.html"):
            downloadFile(data['dl'], data['file'], yearCourses[courseKey], session)
    except Exception as e:
        print(f"connection problem: {e}")

# main program
def runDownloader(local_dir, session, courseKey):
    local_dir = defineDownloadPath(local_dir)
    
    downloadSpecificCourse(courseKey, session, courses[findYear(courses, courseKey)])

    print("Downloads complete!\n")
    os.remove("rawweb.html")