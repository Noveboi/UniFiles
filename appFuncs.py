import updater, downloader
from checker import needsDownload
from json import load
from scraper import getCourseTitle
from fileManager import local_dir

def du(session, courseKey, courseId):
    if needsDownload(courseKey, session):
        print(f"Downloading files from {getCourseTitle(courseId, session)}\n")
        downloader.runDownloader(local_dir, session, courseKey)
    else:
        print(f"Checking for updates on {getCourseTitle(courseId, session)}\n")
        updater.scanCoursesForUpdates(session, courseId, specificCourse=courseKey)

def duSpecific(session):
    with open('courses.json', 'r') as jf:
        courses = load(jf)
    years = ["year_a", "year_b", "year_c", "year_d"]
    isCourse = False
    for year in years:
        while not isCourse:
            courseChoice = input("Enter a valid course key: ")
            for course in courses[year]:
                if courseChoice.lower().strip() == course: 
                    isCourse = True
                    break
        break
    du(session, courseChoice, courses[year][courseChoice])
    print("-----------------------------------")

def duAll(session):
    while True:
        yearChoice = input("Year(s) to download (1,2,3,4): ")
        years = []
        if '1' in yearChoice: years.append('year_a')
        elif '2' in yearChoice: years.append('year_b')
        elif '3' in yearChoice: years.append('year_c')
        elif '4' in yearChoice: years.append('year_d')
        if len(years) > 0:
            break
    
    with open('courses.json', 'r') as jf:
        courses = load(jf)
    for year in years:
        yearCourses = courses[year]
        for course in yearCourses:
            du(session, course, yearCourses[course])

    print("----------------------")

def listCourses(session):
    print("Available courses (Course Name - Course Key):\n ")
    with open('courses.json', 'r') as jf:
        courses = load(jf)
    years = ["year_a", "year_b", "year_c", "year_d"]
    for yearNum, year in enumerate(years):
        print(f"\n----Year {yearNum + 1}---")
        yearCourse = courses[year]
        for course in yearCourse:
            print(f"{getCourseTitle(yearCourse[course], session)} - {course}")
    print("-----------------------------------")