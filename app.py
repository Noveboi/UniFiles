#This is the file the user will run, to download or update
import requests
import appFuncs
from updater import determineAutoUpdate, autoEnabled

if __name__ == "__main__":

    with requests.Session() as session:
        print("Hello! \n---------")
        if autoEnabled: determineAutoUpdate()
        
        while True:
            print("F - View available courses")
            print("D - Download or update specific course")
            print("A - Download or update all courses of year(s)")
            print("E - Exit\n")
            choice = input()
            if choice.lower() == 'f':
                appFuncs.listCourses(session)
            elif choice.lower() == 'e': 
                break
            elif choice.lower() == 'd':
                appFuncs.duSpecific(session)
            elif choice.lower() == 'a':
                appFuncs.duAll(session)

