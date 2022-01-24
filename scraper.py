from bs4 import BeautifulSoup
from os import remove

docDir = "https://gunet2.cs.unipi.gr/modules/document/document.php?course="

def sanitizeText(text):
    text.replace("\n", "")
    return text.strip()

def getTableData(html_file):
    with open(html_file, "r", encoding='utf8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'lxml')
        table = soup.find('table', class_='tbl_alt')
        trows = table.find_all('tr')

        for row in trows[1:]:
            tds = row.find_all('td')
            td = None
            for td in tds:
                pass
            last_td = td

            second_td = tds[1]
            td_a = second_td.find('a')

            file_name = sanitizeText(td_a.text)
            file_link = td_a['href']

            download_link = last_td.find('a')
            yield {
                'file': file_name,
                'dl': download_link['href'],
                'date': tds[-2]['title'],
                'link': file_link
            }

def getCourseTitle(courseId, session):

    courseUrl = f"{docDir}{courseId}"
    r = session.get(courseUrl, verify="cert/gunet2-cs-unipi-gr-chain.pem")
    with open("dump.html", 'w') as html:
        html.write(r.text)
    
    with open("dump.html", 'r') as html:
        content = html.read()
        soup = BeautifulSoup(content, 'lxml')
        lesson_div = soup.find('div', class_="lesson")
        course_title = lesson_div.findChild('a')

    remove("dump.html")
    return course_title.text