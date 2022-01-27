#determine if course directory has already been downloaded
from gettext import find
from fileManager import local_dir
from json import load
from scraper import getCourseTitle
from os import path

def findYear(courseList, courseKey):
    years = ["year_a", "year_b", "year_c", "year_d"]
    for year in years:
        for course in courseList[year]:
            if course == courseKey:
                return year

def needsDownload(courseKey, session):
    with open('courses.json', 'r') as jf:
        courses = load(jf)
    courseFolder = getCourseTitle(courses[findYear(courses,courseKey)][courseKey], session)
    if '/' in courseFolder:
        courseFolder = courseFolder.replace('/', '|')
    courseDir = path.join(local_dir, courseFolder)
    if path.exists(courseDir): return False
    return True