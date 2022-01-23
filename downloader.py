import platform
import requests
import os
from bs4 import BeautifulSoup
import zipfile
from platform import system
import json
from getpass import getuser

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

USER = getuser()
SSL_CERT = "cert/gunet2-cs-unipi-gr-chain.pem" #certificate for SSL handshake 
ENC = "utf8"

c_path = False
home_dir = "https://gunet2.cs.unipi.gr"
documents_dir = "https://gunet2.cs.unipi.gr/modules/document/document.php?course="

os_system = platform.system()
#create default directories 
with open('config.json', 'r', encoding=ENC) as f:
    d = json.load(f)
    if d['custom_path'] == '':
        if os_system == 'Linux':
            local_dir = f"/home/{USER}/Documents/uni_files"  
        else:
            local_dir = f"C:/Users/{USER}/Documents/uni_files"
    else: 
        local_dir = d['custom_path'] #no path check since it's already done in __main__
        c_path = True

file_names = []

def sanitizeText(text):
    text.replace("\n", "")
    return text.strip()

def isZipFile(file):
    if '.' not in file: return True
    return False

def downloadFile(file, download_url, rq, dir):
    substr = download_url[-10:len(download_url)] #-10 index is random, just big enough to cover the extensions

    if isZipFile(substr):
        with open(f"{dir}/{file}.zip", "wb") as f:
            print(f"Downloading {dir}/{file}.zip...")
            f.write(rq.content) 
            print(f"{dir}/{file}.zip downloaded")
    else:
        with open(f"{dir}/{file}", "wb") as f:
            print(f"Downloading {dir}/{file}...")
            f.write(rq.content)
            print(f"{dir}/{file} downloaded")

#a generator which returns each and every download link of a course
def getDownloadLinks(html_file):
    with open(html_file, "r", encoding=ENC) as f:
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
        if not os.path.exists(local_subdir): os.mkdir(local_subdir)
        
        downloadFile(file_name, target_url, rq, local_subdir)
    except Exception as e3:
            print(f"problem with directories: {e3}")

def unzipAndOrganize(file_name, local_subdir):
    try:
        extract_path = os.path.join(local_subdir, file_name)

        zip_path = os.path.join(local_subdir, f"{file_name}.zip")

        if not os.path.exists(extract_path): os.mkdir(extract_path)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_path)
        os.remove(zip_path)
    except Exception as e:
        print(f"unzipping process error: {e}")

def downloadSpecificCourse(courseKey):

    local_subdir = os.path.join(local_dir, f"{courseKey.title()}")
    targetdocs_url = f"{documents_dir}{yearA[courseKey]}"
    try:
        #establish connection to website
        r = ses.get(targetdocs_url, verify=SSL_CERT)
        
        #write to a temp dummy html file the websites contents
        with open("rawweb.html", "w", encoding=ENC) as f: 
            f.write(BeautifulSoup(r.text, 'lxml').prettify())
        
        i = -1
        #assign appropriate link for GET download request
        for link in getDownloadLinks("rawweb.html"):
            i += 1
            target_url = f"{home_dir}{link}"
            substr = target_url[-8:len(target_url)]
            try:
                d_r = ses.get(target_url, verify=SSL_CERT) #download request

                #store files in appropriate directory
                modifyDirs(local_subdir, file_names[i], target_url, d_r)

                #extract files from every .zip and put them in folders
                if isZipFile(substr):
                    unzipAndOrganize(file_names[i], local_subdir)

            except Exception as e2: print(f"download request went wrong: {e2}")
    except Exception as e: print(f"connection problem: {e}")

def defineDownloadPath(local_dir):
    if not c_path:
        usr_dir = input("Copy paste a path for the files to be stored here (leave empty for default): ")
        if usr_dir != '':
            while True:
                if os.path.exists(usr_dir): break
                else:
                    usr_dir = input("Please enter an existing path: ")
            local_dir = os.path.join(usr_dir, 'uni_files' )    
        
        if not os.path.exists(local_dir): os.mkdir(local_dir)
        storeDir = input("Would you like to use this directory in the future? (y/n)")
        if storeDir.lower() == 'y':
            c_dir = {"custom_path": local_dir}
            json_obj = json.dumps(c_dir)
            with open("config.json", 'w', encoding=ENC) as f:
                f.write(json_obj)
            return local_dir
        return local_dir
    else:
        if not os.path.exists(local_dir): 
            usr_dir = input("Your current custom directory doesn't exist, please enter a valid one: ")
            while True:
                if os.path.exists(usr_dir): break
                else:
                    usr_dir = input("Please enter an existing path: ")
            local_dir = os.path.join(usr_dir, 'uni_files')
        return local_dir



#main program
if __name__ == "__main__":
    #ask for custom directory, if input=blank use default path  
    local_dir = defineDownloadPath(local_dir)
    
    #start a new session (ends when program terminates)
    ses = requests.Session()

    downloadSpecificCourse('cmath')
    
    os.remove("rawweb.html")
    print(f"The following files have been downloaded: {file_names}")