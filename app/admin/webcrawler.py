import re
import requests
from bs4 import BeautifulSoup
from ..models import Career
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
            descrip_list = []
            for x in range(0, len(link2.contents[3].contents[1].contents)):
                if link2.contents[3].contents[1].contents[x].string is not None:
                    descrip_list.append(link2.contents[3].contents[1].contents[x].string)
                else:
                    for y in range(0, len(link2.contents[3].contents[1].contents[x].contents)):
                        descrip_list.append(link2.contents[3].contents[1].contents[x].contents[y].string)

            descrip_list = [x for x in descrip_list if x != "\n"]
            full_descrip = ""
            for z in range(0, len(descrip_list)):
                try:
                    print(descrip_list[z].string)
                    full_descrip = full_descrip + "\n" + descrip_list[z].string
                except AttributeError:
                    pass
                career.description = full_descrip
        print("\nRELATED SKILLS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-skills field-type-taxonomy-term-reference field-label-above'}):
            skill_list = []
            for counter in range(0, len(link2.contents[3])):
                empty_space_deleter = link2.contents[3].contents[counter].string.split()
                if not empty_space_deleter == []:
                    skill_list.append(link2.contents[3].contents[counter].string.strip())
                    career.add_skill_name(link2.contents[3].contents[counter].string.strip())
            print(skill_list)
        print("\nRELATED SUBJECTS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-subjects field-type-taxonomy-term-reference field-label-above'}):
            sub_list = []
            for counter in range(0, len(link2.contents[3])):
                empty_space_deleter = link2.contents[3].contents[counter].string.split()
                if not empty_space_deleter == []:
                    sub_list.append(link2.contents[3].contents[counter].string.strip())
                    career.add_subject_name(link2.contents[3].contents[counter].string.strip())
            print(sub_list)
        print("\nDESIRABLE QUALIFICATIONS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-desirable-qualifications field-type-text field-label-above'}):
            qual_list = []
            for counter in range(0, len(link2.contents[3])):
                empty_space_deleter = link2.contents[3].contents[counter].string.split()
                if not empty_space_deleter == []:
                    qual_list.append(link2.contents[3].contents[counter].string.strip())
                    # career.add_subject_name(link2.contents[3].contents[counter].string.strip())
            print(qual_list)
        db.session.add(career)
        db.session.commit()
