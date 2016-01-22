import re
import requests
from bs4 import BeautifulSoup


def webcrawler():
    url = "https://www.ucas.com/ucas/after-gcses/find-career-ideas/explore-jobs#js=on"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.find_all(href=re.compile("job-profile")):
        title = link.string
        print("\n")
        print(title)
        href = "https://www.ucas.com" + link.get('href')
        print(href)
        source_code2 = requests.get("https://www.ucas.com" + link.get('href'))
        plain_text2 = source_code2.text
        soup2 = BeautifulSoup(plain_text2, "html.parser")
        print("\nRELATED SKILLS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-skills field-type-taxonomy-term-reference field-label-above'}):
            skillList = []
            for counter in range(0, len(link2.contents[3])):
                listofskills = link2.contents[3].contents[counter].string.split()
                if listofskills == []:
                    ++counter
                else:
                    skillList.append(link2.contents[3].contents[counter].string.strip())
            print(skillList)
        print("\nRELATED SUBJECTS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-related-subjects field-type-taxonomy-term-reference field-label-above'}):
            subList = []
            for counter in range(0, len(link2.contents[3])):
                listofskills = link2.contents[3].contents[counter].string.split()
                if listofskills == []:
                    ++counter
                else:
                    subList.append(link2.contents[3].contents[counter].string.strip())
            print(subList)
        print("\nDESIRABLE QUALIFICATIONS")
        for link2 in soup2.find_all('div', {
            'class': 'field field-name-field-desirable-qualifications field-type-text field-label-above'}):
            qualList = []
            for counter in range(0, len(link2.contents[3])):
                listofskills = link2.contents[3].contents[counter].string.split()
                if listofskills == []:
                    ++counter
                else:
                    qualList.append(link2.contents[3].contents[counter].string.strip())
            print(qualList)
