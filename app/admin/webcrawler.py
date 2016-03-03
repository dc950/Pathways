import re
import requests
from bs4 import BeautifulSoup
from ..models import Career, Qualification
from .. import db

def webcrawler():
    url = "https://www.ucas.com/ucas/after-gcses/find-career-ideas/explore-jobs#js=on"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.find_all(href=re.compile("job-profile")):
        title = link.string
        b = False
        for c in Career.query.all():
            if c.name == title:
                b = True
        if b:
            continue
        career = Career()
        print("\n")
        print(title)
        career.name = title
        href = "https://www.ucas.com" + link.get('href')
        print(href)
        career.url = href
        source_code2 = requests.get("https://www.ucas.com" + link.get('href'))
        plain_text2 = source_code2.text
        soup2 = BeautifulSoup(plain_text2, "html.parser")
        print("\nJOB DESCRIPTION")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-job-profile-role field-type-text-long field-label-above prose'}):
            descripList = []
            for x in range(0, len(link2.contents[3].contents[1].contents)):
                if link2.contents[3].contents[1].contents[x].string is not None:
                    descripList.append(link2.contents[3].contents[1].contents[x].string)
                else:
                    for y in range(0,len(link2.contents[3].contents[1].contents[x].contents)):
                        descripList.append(link2.contents[3].contents[1].contents[x].contents[y].string)

            descripList = [x for x in descripList if x != "\n"]
            fullDescrip=""
            for z in range(0,len(descripList)):
                try:
                    print(descripList[z].string)
                    fullDescrip = fullDescrip + "\n" + descripList[z].string
                except AttributeError:
                    ++z
                career.description = fullDescrip
        print("\nRELATED SKILLS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-skills field-type-taxonomy-term-reference field-label-above'}):
            skillList = []
            for counter in range(0, len(link2.contents[3])):
                emptyspacedeleter = link2.contents[3].contents[counter].string.split()
                if emptyspacedeleter == []:
                    ++counter
                else:
                    skillList.append(link2.contents[3].contents[counter].string.strip())
                    career.add_skill_name(link2.contents[3].contents[counter].string.strip())
            print(skillList)
        print("\nRELATED SUBJECTS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-subjects field-type-taxonomy-term-reference field-label-above'}):
            subList = []
            for counter in range(0, len(link2.contents[3])):
                emptyspacedeleter = link2.contents[3].contents[counter].string.split()
                if emptyspacedeleter == []:
                    ++counter
                else:
                    subList.append(link2.contents[3].contents[counter].string.strip())
                    career.add_subject_name(link2.contents[3].contents[counter].string.strip())
            print(subList)
        print("\nDESIRABLE QUALIFICATIONS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-desirable-qualifications field-type-text field-label-above'}):
            qualList = []
            for counter in range(0, len(link2.contents[3])):
                emptyspacedeleter = link2.contents[3].contents[counter].string.split()
                if emptyspacedeleter == []:
                    ++counter
                else:
                    qualList.append(link2.contents[3].contents[counter].string.strip())
                    career.add_subject_name(link2.contents[3].contents[counter].string.strip())
            print(qualList)
        db.session.add(career)
        db.session.commit()