import requests
import os
from bs4 import BeautifulSoup
from scraper import getTableData
from fileManager import isFolder, modifyDirs, unzipAndOrganize, defineDownloadPath, local_dir

yearA = {
    'anal1': "TMA117",
    'anal2': "TMA120",
    'oop': "TMA103",
    'cpp': "TMA105",
    'arch': "TMA106",
    'disc': "TMA113",
    'data': "TMA114",
    'appl': "TMA119",
    'logic': "TMA108",
    'cmath': "TMA123",
    'wtech': "TMA110",
    'pyth': "TMA111"
}

SSL_CERT = "cert/gunet2-cs-unipi-gr-chain.pem"  # certificate for SSL handshake
ENC = "utf8"

home_dir = "https://gunet2.cs.unipi.gr"
documents_dir = "https://gunet2.cs.unipi.gr/modules/document/document.php?course="

def downloadFile(file_path,file_name,courseKey):
    local_subdir = os.path.join(local_dir, f"{courseKey.title()}")
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

def downloadSpecificCourse(courseKey):
    targetdocs_url = f"{documents_dir}{yearA[courseKey]}"
    try:
        # establish connection to website
        r = session.get(targetdocs_url, verify=SSL_CERT)

        # write to a temp dummy html file the websites contents
        with open("rawweb.html", "w", encoding=ENC) as f:
            f.write(BeautifulSoup(r.text, 'lxml').prettify())

        # assign appropriate link for GET download request
        for data in getTableData("rawweb.html"):
            downloadFile(data['dl'], data['file'], courseKey)
    except Exception as e:
        print(f"connection problem: {e}")

session = requests.Session()

# main program
def runDownloader(local_dir):
    # ask for custom directory, if input=blank use default path
    local_dir = defineDownloadPath(local_dir)
    
    downloadSpecificCourse('anal1')

    os.remove("rawweb.html")