import requests
from bs4 import BeautifulSoup
#from ..models import Career, Qualification
#from .. import db

def uniwebcrawler():
    for counter in range(1, 8):
        #unicourses = UniCourses()
        url = "http://university.which.co.uk/search/course?c[institution_name_tag__and__some]=heriot_watt_university&c[sort_fact]=title&c[page]="+str(counter)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.find_all('h6', {'class': 'result-card__heading-sub course-name'}):
            coursetitle= link.contents[0].contents
            print(coursetitle)
            for link2 in link.find_all('a'):
                print(link2.get('href'))
                ++counter
                source_code2 = requests.get("http://university.which.co.uk" + link2.get('href'))
                plain_text2 = source_code2.text
                soup2 = BeautifulSoup(plain_text2, "html.parser")
                for link3 in soup2.find('div', {'class': 'summary-block-section-bottom'}):
                    ucaspoints = link3.string
                    if(ucaspoints == "\n"):
                        continue
                    else:
                        maxucaspoints = str(ucaspoints)
                        minucaspoints =  str(ucaspoints)
                        print(maxucaspoints[4:])
                        print(minucaspoints[:3])
                for link3 in soup2.find_all('span', {'class': 'scheme'}):
                    nameofcourse = link3.contents[0]
                    if(nameofcourse=="A level"):
                        alevels = link3.parent.parent.contents[3].contents[1].contents[0].string
                        print(alevels.split("-",1)[0])
                    elif(nameofcourse=="Scottish Highers"):
                        highers = link3.parent.parent.contents[3].contents[1].contents[0].string#
                        print(highers.split("-",1)[0])
                    elif(nameofcourse==" Scottish Advanced Highers"):
                        advhighers = link3.parent.parent.contents[3].contents[1].contents[0].string
                        print(advhighers.split("-",1)[0])
                    elif(nameofcourse=="International Baccalaureate"):
                        intbacc = link3.parent.parent.contents[3].contents[1].contents[0].string
                        print(intbacc.split("-",1)[0])

uniwebcrawler()