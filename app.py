#This is the file the user will run, to download or update
import requests
import appFuncs
from updater import determineAutoUpdate, autoEnabled
from fileManager import checkIfDirExists, local_dir

if __name__ == "__main__":

    with requests.Session() as session:
        print("Hello! \n---------")

        checkIfDirExists(local_dir)
        if autoEnabled: determineAutoUpdate(session)
        #program loop
        while True:
            print("F1-4 - View available for specific year (f without number for all years)")
            print("D - Download or update specific course")
            print("A - Download or update all courses of year(s)")
            print("E - Exit\n")
            choice = input()
            if choice.lower().strip()[0] == 'f':
                if len(choice.strip()) > 1:
                    if choice.strip()[1].isdigit():
                        if int(choice.strip()[1]) <= 4:
                            appFuncs.listCourses(session, year=int(choice.strip()[1]))
                else:
                    appFuncs.listCourses(session)
            elif choice.lower() == 'e': 
                print("\nBye!\n")
                break
            elif choice.lower() == 'd':
                appFuncs.duSpecific(session)
            elif choice.lower() == 'a':
                appFuncs.duAll(session)

