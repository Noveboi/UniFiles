import os
import zipfile
import json
from platform import system
from getpass import getuser

c_path = False
SYS = system()
USER = getuser()


# create default directories
with open('config.json', 'r', encoding='utf8') as f:
    d = json.load(f)
    if d['custom_path'] == '':
        if SYS == 'Linux':
            local_dir = f"/home/{USER}/Documents/uni_files"
        else:
            local_dir = f"C:/Users/{USER}/Documents/uni_files"
    else:
        # no path check since it's already done in __main__
        local_dir = d['custom_path']
        c_path = True

def isFolder(file):
    if '.' not in file[-8:len(file)]:
        return True
    return False

def dlAndWriteToFile(file, download_url, rq, dir):
    if isFolder(download_url):
        print(f"Downloading {file}.zip...")
        with open(f"{dir}/{file}.zip", "wb") as f:
            f.write(rq.content)
            print(f"{file}.zip downloaded\n")
    else:
        print(f"Downloading {file}...")
        with open(f"{dir}/{file}", "wb") as f:
            f.write(rq.content)
            print(f"{file} downloaded\n")

def modifyDirs(local_subdir, file_name, target_url, rq):
    try:
        if not os.path.exists(local_subdir):
            os.mkdir(local_subdir)

        dlAndWriteToFile(file_name, target_url, rq, local_subdir)
    except Exception as e3:
        print(f"problem with directories: {e3}")

def unzipAndOrganize(file_name, local_subdir):
    try:
        extract_path = os.path.join(local_subdir, file_name)

        zip_path = os.path.join(local_subdir, f"{file_name}.zip")

        if not os.path.exists(extract_path):
            os.mkdir(extract_path)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_path)
        os.remove(zip_path)
    except Exception as e:
        print(f"unzipping process error: {e}")

def defineDownloadPath(local_dir):
    if not c_path:
        usr_dir = input(
            "Copy paste a path for the files to be stored here (leave empty for default): ")
        if usr_dir != '':
            while True:
                if os.path.exists(usr_dir):
                    break
                else:
                    usr_dir = input("Please enter an existing path: ")
            local_dir = os.path.join(usr_dir, 'uni_files')

        if not os.path.exists(local_dir):
            os.mkdir(local_dir)
        storeDir = input(
            "Would you like to use this directory in the future? (y/n)")
        if storeDir.lower() == 'y':
            c_dir = {"custom_path": local_dir}
            json_obj = json.dumps(c_dir)
            with open("config.json", 'w', encoding='utf8') as f:
                f.write(json_obj)
            return local_dir
        return local_dir
    else:
        if not os.path.exists(local_dir):
            usr_dir = input(
                "Your current custom directory doesn't exist, please enter a valid one: ")
            while True:
                if os.path.exists(usr_dir):
                    c_dir = {"custom_path": local_dir}
                    json_obj = json.dumps(c_dir)
                    with open("config.json", 'w', encoding='utf8') as f:
                        f.write(json_obj)
                    break
                else:
                    usr_dir = input("Please enter an existing path: ")
            local_dir = os.path.join(usr_dir, 'uni_files')
        return local_dir