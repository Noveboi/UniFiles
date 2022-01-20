from threading import local
import requests
import os
from bs4 import BeautifulSoup
import zipfile

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
    'wtech': "TMA110"
}

USER = os.environ['USER']
SSL_CERT = "cert/gunet2-cs-unipi-gr-chain.pem" #certificate for SSL handshake 

home_dir = "https://gunet2.cs.unipi.gr"
documents_dir = "https://gunet2.cs.unipi.gr/modules/document/document.php?course="
local_dir = f"/home/{USER}/Desktop/test_flder/" #for linux
file_names = []

def sanitizeText(text):
    text.replace("\n", "")
    return text.strip()

def downloadFile(file, download_url, rq, dir):
    substr = download_url[-10:len(download_url)] #-10 index is random, just big enough to cover the extensions

    if '.' not in substr:
        with open(f"{dir}/{file}.zip", "wb") as f:
            f.write(rq.content) 
        print(f"{dir}/{file}.zip downloaded")
    else:
        # extension = substr[substr.index('.'):len(substr)]
        with open(f"{dir}/{file}", "wb") as f:
            f.write(rq.content)
        print(f"{dir}/{file}")

#a generator which returns each and every download link of a course
def getDownloadLinks(html_file):
    with open(html_file, "r") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'lxml')
        table = soup.find('table', class_='tbl_alt')
        trows = table.find_all('tr')

        for row in trows[1:]:
            tds = row.find_all('td')
            td = None
            for td in tds: pass
            last_td = td

            second_td = tds[1]
            td_a = second_td.find('a')

            file_name = sanitizeText(td_a.text)

            file_names.append(file_name)

            download_link = last_td.find('a')
            yield download_link['href']

def modifyDirs(local_subdir, file_name, target_url, rq):
    try:
        if os.path.exists(local_subdir):
            downloadFile(file_name, target_url, rq, local_subdir)
        else:
            os.mkdir(local_subdir)
            downloadFile(file_name, target_url, rq, local_subdir)
    except Exception as e3:
            print(f"problem with directories: {e3}")

def unzipAndOrganize(file_name, local_subdir):
    if '.' in file_name:
        extract_path = os.path.join(local_subdir, file_name[0:file_name.index('.')])
        #e.g - hello.pdf becomes hello

    zip_path = os.path.join(local_subdir, file_name)

    if os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_path)
    else:
        os.mkdir(extract_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_path)

def downloadSpecificCourse(courseKey):

    local_subdir = os.path.join(local_dir, f"{courseKey.title()}")
    targetdocs_url = f"{documents_dir}{yearA[courseKey]}"
    try:
        #establish connection to website
        r = ses.get(targetdocs_url, verify=SSL_CERT)
        
        #write to a temp dummy html file the websites contents
        with open("rawweb.html", "w") as f: 
            f.write(BeautifulSoup(r.text, 'lxml').prettify())
        
        i = -1
        #assign appropriate link for GET download request
        for link in getDownloadLinks("rawweb.html"):
            i += 1
            target_url = f"{home_dir}{link}"
            try:
                d_r = ses.get(target_url, verify=SSL_CERT) #download request

                #store files in appropriate directory
                modifyDirs(local_subdir, file_names[i], target_url, d_r)

                #extract files from every .zip and put them in folders
                unzipAndOrganize(file_names[i], local_subdir)

            except Exception as e2: print(f"download request went wrong: {e2}")
    except Exception as e: print(f"connection problem: {e}")

#main program
if __name__ == "__main__":
    #start a new session
    ses = requests.Session()

    downloadSpecificCourse('anal1')
    
    os.remove("rawweb.html")
    print(f"The following files are to be downloaded: {file_names}")