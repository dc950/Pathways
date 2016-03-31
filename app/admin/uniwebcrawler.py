import requests
from bs4 import BeautifulSoup
from ..models import Qualification, Subject, QualificationType
from .. import db


def uniwebcrawler():
    print("In uni crawler")
    for counter in range(1, 8):
        url = "http://university.which.co.uk/search/course?c[institution_name_tag__and__some]=heriot_watt_university&c[sort_fact]=title&c[page]=" + str(
            counter)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.find_all('h6', {'class': 'result-card__heading-sub course-name'}):
            course_title = link.contents[0].contents[0]
            b = False
            for q in Qualification.query.all():
                if q.name == course_title:
                    b = True
            if b:
                continue
            qualification = Qualification()
            subject = Subject.new_subject(course_title)
            qualification_type = QualificationType.newType("Bachelor's Degree")
            qualification.subject = subject
            qualification.qualification_type = qualification_type
            print(course_title)
            for link2 in link.find_all('a'):
                print(link2.get('href'))
                source_code2 = requests.get("http://university.which.co.uk" + link2.get('href'))
                plain_text2 = source_code2.text
                soup2 = BeautifulSoup(plain_text2, "html.parser")
                for link3 in soup2.find('div', {'class': 'summary-block-section-bottom'}):
                    ucaspoints = link3.string
                    if ucaspoints == "\n":
                        continue
                    else:
                        maxupoints = str(ucaspoints)
                        minupoints = str(ucaspoints)
                        qualification.maxucaspoints = maxupoints[4:]
                        qualification.minucaspoints = minupoints[:3]
                        print(maxupoints[4:])
                        print(minupoints[:3])
                for link3 in soup2.find_all('span', {'class': 'scheme'}):
                    nameofcourse = link3.contents[0]
                    if nameofcourse == "A level":
                        alevels = link3.parent.parent.contents[3].contents[1].contents[0].string
                        qualification.alevelgrades = alevels.split("-", 1)[0]
                        print("alevels " + alevels.split("-", 1)[0])
                    elif nameofcourse == "Scottish Highers":
                        highers = link3.parent.parent.contents[3].contents[1].contents[0].string
                        qualification.highers = highers.split("-", 1)[0]
                        print("highers " + highers.split("-", 1)[0])
                    elif nameofcourse == "Scottish Advanced Highers":
                        advhighers = link3.parent.parent.contents[3].contents[1].contents[0].string
                        qualification.advancedhighers = advhighers.split("-", 1)[0]
                        print("adv high " + advhighers.split("-", 1)[0])
                    elif nameofcourse == "International Baccalaureate":
                        intbacc = link3.parent.parent.contents[3].contents[1].contents[0].string
                        qualification.internationalbaccalaureate = intbacc.split("-", 1)[0]
                        print("int bacc " + intbacc.split("-", 1)[0])

            db.session.add(qualification)
    db.session.commit()
