from ..models import QualificationType, Qualification, Subject, Field, Role
from .webcrawler import webcrawler
from .uniwebcrawler import uniwebcrawler
from .. import db

gcse = QualificationType()
btec2 = QualificationType()
a_level = QualificationType()
btec3 = QualificationType()
higher = QualificationType()
btec4 = QualificationType()
cert_higher_ed = QualificationType()
adv_higher = QualificationType()
diploma = QualificationType()
btec5 = QualificationType()
foundation_degree = QualificationType()
bachelors_degree = QualificationType()
masters_degree = QualificationType()
phd = QualificationType()


def setup(clear=False):
    if clear is True:
        QualificationsClear()

    DefineFields()
    print("****   Define Fields Complete   ****")
    DefineQualificationTypes()
    print("****   Define Qualification Types Complete   ****")
    DefineSubjects()
    Role.insert_roles()
    print("****   Define Subjects Complete   ****")
    webcrawler()
    print("****   Career Crawler Complete   ****")
    uniwebcrawler()
    print("****   University Crawler Complete   ****")
    DefineQualifications()


def QualificationsClear():
    QualificationType.query.delete()
    Field.query.delete()
    Subject.query.delete()
    Qualification.query.delete()

    db.session.commit()


def DefineQualifications():
    print("Test")


def DefineQualificationTypes():


    """ 1 Added """
    global gcse
    gcse.name = "GCSE"
    gcse.level = 2
    db.session.add(gcse)
    gcse.allowed_grades = '^(A\*|[A-FU])$'
    #make_transient(gcse)

    """ 2 """
    # global btec2
    # btec2.name = "BTEC Level 2"
    # btec2.level = 2
    # db.session.add(btec2)
    # #make_transient(btec2)

    """ 3 """
    # global a_level
    # a_level.name = "A-Level"
    # a_level.level = 3
    # db.session.add(a_level)
    # #make_transient(a_level)

    """ 4 """
    # global btec3
    # btec3.name = "BTEC Level 3"
    # btec3.level = 3
    # db.session.add(btec3)
    # #make_transient(btec3)

    """ 5 Added """
    global higher
    higher.name = "Scottish Higher"
    higher.level = 3
    db.session.add(higher)
    higher.allowed_grades = '^[A-DF]$'
    #make_transient(higher)

    """ 6 """
    # global btec4
    # btec4.name = "BTEC Level 4"
    # btec4.level = 4
    # db.session.add(btec4)
    # #make_transient(btec4)

    """ 7 """
    # global cert_higher_ed
    # cert_higher_ed.name = "Certificate of Higher Education"
    # cert_higher_ed.level = 4
    # db.session.add(cert_higher_ed)
    # #make_transient(cert_higher_ed)

    """ 8 Added """
    global adv_higher
    adv_higher.name = "Scottish Advanced Higher"
    adv_higher.level = 4
    db.session.add(adv_higher)
    adv_higher.allowed_grades = '^[A-DF]$'
    #make_transient(adv_higher)

    """ 9 """
    # global diploma
    # diploma.name = "Diploma"
    # diploma.level = 4
    # db.session.add(diploma)
    # #make_transient(diploma)

    """ 10 """
    # global btec5
    # btec5.name = "BTEC Level 5"
    # btec5.level = 5
    # db.session.add(btec5)
    # #make_transient(btec5)

    """ 11 """
    # global foundation_degree
    # foundation_degree.name = "Foundation Degree"
    # foundation_degree.level = 5
    # db.session.add(foundation_degree)
    # #make_transient(foundation_degree)

    """ 12 """
    global bachelors_degree
    bachelors_degree.name = "Bachelor's Degree"
    bachelors_degree.level = 6
    db.session.add(bachelors_degree)
    bachelors_degree.allowed_grades = '^(1st|2:[12]|3rd|pass)$'
    #make_transient(bachelors_degree)

    """ 13 """
    global masters_degree
    masters_degree.name = "Master's Degree"
    masters_degree.level = 7
    db.session.add(masters_degree)
    masters_degree.allowed_grades = '^(1st|2:[12]|3rd|pass)$'
    #make_transient(masters_degree)

    """ 14 """
    global phd
    phd.name = "PhD"
    phd.level = 8
    db.session.add(phd)
    phd.allowed_grades = '^(pass|fail)$'
    #make_transient(phd)

    db.session.commit()

    

def DefineSubjects():



    for subject in [["English", "Literature"], ["English Language", "Linguistics"], ["English Literature", "Literature"], ["Mathematics", "Mathematics"], ["Welsh", "Linguistics"], ["Welsh Second Language", "Linguistics"], 
                ["Welsh Language", "Linguistics"],  ["Irish", "Linguistics"],  ["Science", "Earth Sciences"], ["Biology", "Biology"], ["Chemistry", "Chemistry"], ["Physics", "Physics"], ["Core Science", "Earth Sciences"], 
                ["Double Science", "Earth Sciences"], ["Triple Science", "Earth Sciences"], ["Additional Science", "Earth Sciences"], ["Afrikaans", "Linguistics"], ["Arabic", "Linguistics"], ["Bengali", "Linguistics"], 
                ["Cantonese", "Linguistics"], ["Mandarin", "Linguistics"], ["Dutch", "Linguistics"], ["French", "Linguistics"], ["Applied French", "Linguistics"],  ["Business French", "Linguistics"], 
                ["German", "Linguistics"], ["Applied German", "Linguistics"], ["Business German", "Linguistics"], ["Modern Greek", "Linguistics"], ["Gujarati", "Linguistics"], ["Modern Hebrew", "Linguistics"], 
                ["Hindi", "Linguistics"],  ["Gaeilge", "Linguistics"], ["Italian", "Linguistics"], ["Japanese", "Linguistics"], ["Maltese", "Linguistics"], ["Malay", "Linguistics"], ["Manx", "Linguistics"], 
                ["Punjabi", "Linguistics"], ["Persian", "Linguistics"], ["Polish", "Linguistics"],  ["Portuguese", "Linguistics"], ["Russian", "Linguistics"],  ["Somali", "Linguistics"], ["Spanish", "Linguistics"], 
                ["Tamil", "Linguistics"], ["Telugu", "Linguistics"], ["Turkish", "Linguistics"], ["Urdu", "Linguistics"], ["Yoruba", "Linguistics"],   ["Classical Tamil", "Linguistics"], ["Classical Arabic", "Linguistics"], 
                ["Classical Greek", "Linguistics"], ["Biblical Hebrew", "Linguistics"], ["Latin", "Linguistics"], ["Classical Sanskrit", "Linguistics"],   ["Design & Technology", "Architecture & Design"], 
                ["Parametric CAD", "Engineering & Technology"], ["Electronic Products", "Engineering & Technology"], ["Electronics", "Engineering & Technology"], ["Food Technology", "Agriculture"],  
                ["Graphic Design/Products", "Visual Arts"],  ["Product Design", "Architecture & Design"], ["Resistant Materials", "Engineering & Technology"], ["Textiles", "Visual Arts"], ["Product Design", "Visual Arts"], 
                ["Resistant Materials", "Architecture & Design"], ["Textiles", "Visual Arts"], ["Systems & Control", "Engineering & Technology"],  ["Catering", "Agriculture"], 
                ["Electronics with Resistant Materials", "Engineering & Technology"], ["Engineering", "Engineering & Technology"], ["Engineering & Manufacturing", "Engineering & Technology"], ["Home Economics", "Agriculture"],  
                ["Food & Nutrition", "Agriculture"], ["Child Development", "Social Work"], ["Textiles", "Visual Arts"], ["Manufacturing", "Engineering & Technology"], ["ICT", "Computer Science"], ["Computer Science", "Computer Science"], 
                ["Computing", "Computer Science"],  ["Digital technology", "Computer Science"],   ["Citizenship", "Anthropology"], ["Classical Civilisation", "Human History"], ["Economics", "Economics"], ["Geography", "Geography"], 
                ["History", "Human History"], ["Humanities", "Anthropology"], ["Religious Studies", "Religious Studies"], ["Buddhism", "Religious Studies"],  ["Christianity", "Religious Studies"], ["Hinduism", "Religious Studies"], 
                ["Islam", "Religious Studies"], ["Judaism", "Religious Studies"], ["Philosophy & Ethics", "Philosophy"], ["Sikhism", "Religious Studies"],  ["Business Studies", "Business"], ["Applied Business", "Business"], 
                ["Business & Economics", "Business"], ["Business & Communications Systems", "Business"], ["Financial Services", "Economics"],  ["Health & Social Care", "Social Work"], ["Hospitality", "Sociology"], ["Law", "Law"],
                ["Leisure & Tourism", "Geography"], ["Psychology", "Psychology"], ["Sociology", "Sociology"], ["Travel & Tourism", "Geography"],  ["Animation", "Visual Arts"], ["Applied Art & Design", "Visual Arts"],
                ["Art & Design", "Visual Arts"], ["Fine Art", "Visual Arts"], ["Graphics", "Visual Arts"], ["Photography", "Visual Arts"], ["Textiles", "Visual Arts"], ["3D Design", "Visual Arts"], ["Dance", "Visual Arts"],
                ["Drama", "Performing Arts"], ["Digital Photography", "Visual Arts"], ["Expressive Arts", "Performing Arts"], ["Film Studies", "Journalism, Media Studies & Communication"], ["Media Studies", "Journalism, Media Studies & Communication"],
                ["Moving Image Arts", "Performing Arts"], ["Music", "Performing Arts"],  ["Performing Arts", "Performing Arts"], ["Original Writing", "Literature"],  ["Accounting", "Business"], 
                ["Additional Mathematics", "Mathematics"], ["Astronomy", "Physics"], ["Construction", "Architecture & Design"], ["Construction & the Built Environment", "Architecture & Design"],  
                ["Environmental Science", "Environmental Studies"], ["Geology", "Geography"], ["General Studies", "Sociology"], ["Human Physiology & Health", "Human Physical Performance & Recreation"], 
                ["IFS Personal Finance", "Economics"], ["Journalism", "Journalism, Media Studies & Communication"],  ["Learning for Life & Work", "Sociology"], ["Motorsport", "Engineering & Technology"], ["Motor Vehicle & Road User Studies", "Engineering & Technology"],
                ["Personal & Social Education", "Sociology"],  ["Physical Education", "Human Physical Performance & Recreation"], ["Preparation for Working Life", "Sociology"], ["Rural & Agricultural Science", "Agriculture"],
                ["Statistics", "Mathematics"]]:        
        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = gcse
        db.session.add(s)
        db.session.add(q)



    for subject in [["Accounting", "Economics"], ["Administration", "Public Administration"], ["Architectural Technology", "Architecture & Design"], ["Art & Design", "Visual Arts"], ["Automotive Engineering", "Engineering & Technology"], ["Biology", "Biology"], 
                ["Biotechnology", "Computer Science"], ["Building & Architectural Technology", "Architecture & Design"], ["Building Services", "Engineering & Technology"], ["Business Management", "Business"], ["Care", "Social Work"], ["Chemistry", "Chemistry"], 
                ["Civil Engineering", "Engineering & Technology"], ["Classical Greek", "Linguistics"], ["Classical Studies", "Linguistics"], ["Chinese Language & Culture", "Linguistics"], ["Computing", "Computer Science"], ["Construction", "Engineering & Technology"], 
                ["Dance", "Performing Arts"], ["Drama", "Performing Arts"], ["Early Education & Childcare", "Education"], ["Early Years Care & Education", "Education"], ["Economics", "Economics"], ["Electrical Engineering", "Engineering & Technology"], 
                ["Electronics", "Engineering & Technology"], ["English", "Literature"], ["English for Speakers of Other Languages", "Linguistics"], ["Fabrication & Welding Engineering", "Engineering & Technology"], ["French", "Linguistics"], ["Gaelic", "Linguistics"], 
                ["Gàidhlig", "Linguistics"], ["Geography", "Geography"], ["Geology", "Geography"], ["German", "Linguistics"], ["Graphic Communication", "Visual Arts"], ["History", "Human History"], 
                ["Home Economics: Fashion & Textile Technology", "Visual Arts"], ["Home Economics: Health & Food Technology", "Agriculture"], 
                ["Home Economics: Lifestyle & Consumer Technology", "Family & Consumer Science"], ["Hospitality: Food & Drink Service", "Agriculture"], ["Hospitality: Professional Cookery", "Agriculture"], 
                ["Hospitality: Reception & Accommodation Operations", "Sociology"], ["Human Biology", "Biology"], ["Information Systems", "Computer Science"], ["Italian", "Linguistics"], ["Land Use", "Geography"], ["Latin", "Linguistics"], 
                ["Managing Environmental Resources", "Organisational Studies"], ["Mandarin Chinese", "Linguistics"], ["Manufacturing", "Engineering & Technology"], ["Mathematics", "Mathematics"], ["Mechanical Engineering", "Engineering & Technology"], 
                ["Mechatronics", "Engineering & Technology"], ["Media Studies", "Journalism, Media Studies & Communication"], ["Modern Studies", "Anthropology"], ["Music", "Performing Arts"], ["Personal & Social Education", "Education"], ["Philosophy", "Philosophy"], ["Photography", "Visual Arts"], 
                ["Physical Education", "Human Physical Performance & Recreation"], ["Physics", "Physics"], ["Politics", "Political Science"], ["Product Design", "Architecture & Design"], ["Psychology", "Psychology"], ["Religious Education", "Religious Studies"], 
                ["Religious, Moral & Philosophical Studies", "Religious Studies"], ["Russian", "Linguistics"], ["Sociology", "Sociology"], ["Spanish", "Linguistics"], ["Technological Studies", "Computer Science"], ["Travel & Tourism", "Geography"], 
                ["Urdu", "Linguistics"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = higher
        db.session.add(s)
        db.session.add(q)

    for subject in [["Accounting", "Economics"], ["Administration", "Public Administration"], ["Architectural Technology", "Architecture & Design"], ["Art & Design", "Visual Arts"], ["Automotive Engineering", "Engineering & Technology"], ["Biology", "Biology"],
                ["Biotechnology", "Computer Science"], ["Building & Architectural Technology", "Architecture & Design"], ["Building Services", "Engineering & Technology"], ["Business Management", "Business"], ["Care", "Social Work"], ["Chemistry", "Chemistry"],
                ["Civil Engineering", "Engineering & Technology"], ["Classical Greek", "Linguistics"], ["Classical Studies", "Linguistics"], ["Chinese Language & Culture", "Linguistics"], ["Computing", "Computer Science"], ["Construction", "Engineering & Technology"],
                ["Dance", "Performing Arts"], ["Drama", "Performing Arts"], ["Early Education & Childcare", "Education"], ["Early Years Care & Education", "Education"], ["Economics", "Economics"], ["Electrical Engineering", "Engineering & Technology"],
                ["Electronics", "Engineering & Technology"], ["English", "Literature"], ["English for Speakers of Other Languages", "Linguistics"], ["Fabrication & Welding Engineering", "Engineering & Technology"], ["French", "Linguistics"], ["Gaelic", "Linguistics"],
                ["Gàidhlig", "Linguistics"], ["Geography", "Geography"], ["Geology", "Geography"], ["German", "Linguistics"], ["Graphic Communication", "Visual Arts"], ["History", "Human History"],
                ["Home Economics: Fashion & Textile Technology", "Visual Arts"], ["Home Economics: Health & Food Technology", "Agriculture"],
                ["Home Economics: Lifestyle & Consumer Technology", "Family & Consumer Science"], ["Hospitality: Food & Drink Service", "Agriculture"], ["Hospitality: Professional Cookery", "Agriculture"],
                ["Hospitality: Reception & Accommodation Operations", "Sociology"], ["Human Biology", "Biology"], ["Information Systems", "Computer Science"], ["Italian", "Linguistics"], ["Land Use", "Geography"], ["Latin", "Linguistics"],
                ["Managing Environmental Resources", "Organisational Studies"], ["Mandarin Chinese", "Linguistics"], ["Manufacturing", "Engineering & Technology"], ["Mathematics", "Mathematics"], ["Mechanical Engineering", "Engineering & Technology"],
                ["Mechatronics", "Engineering & Technology"], ["Media Studies", "Journalism, Media Studies & Communication"], ["Modern Studies", "Anthropology"], ["Music", "Performing Arts"], ["Personal & Social Education", "Education"], ["Philosophy", "Philosophy"], ["Photography", "Visual Arts"],
                ["Physical Education", "Human Physical Performance & Recreation"], ["Physics", "Physics"], ["Politics", "Political Science"], ["Product Design", "Architecture & Design"], ["Psychology", "Psychology"], ["Religious Education", "Religious Studies"],
                ["Religious, Moral & Philosophical Studies", "Religious Studies"], ["Russian", "Linguistics"], ["Sociology", "Sociology"], ["Spanish", "Linguistics"], ["Technological Studies", "Computer Science"], ["Travel & Tourism", "Geography"],
                ["Urdu", "Linguistics"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = a_level
        db.session.add(s)
        db.session.add(q)

    for subject in [["Accounting", "Economics"], ["Administration", "Organisational Studies"], ["Applied Mathematics: Mechanics", "Mathematics"], ["Applied Mathematics: Statistics", "Mathematics"],
                    ["Art & Design Enquiry: Design", "Visual Arts"], ["Art & Design Enquiry: Expressive", "Visual Arts"], ["Art & Design: Research & Appreciation", "Anthropology"],
                    ["Biology", "Biology"], ["Building & Architectural Technology", "Architecture & Design"], ["Business Management", "Business"], ["Chemistry", "Chemistry"],
                    ["Civil Engineering", "Engineering & Technology"], ["Classical Greek", "Linguistics"], ["Classical Studies", "Literature"], ["Computing", "Computer Science"],
                    ["Drama", "Performing Arts"], ["Economics", "Economics"], ["Electronics", "Engineering & Technology"], ["English", "Literature"], ["French", "Linguistics"],
                    ["Gaelic", "Linguistics"], ["Gaidhlig", "Linguistics"], ["Geography", "Geography"], ["Geology", "Geography"], ["German", "Linguistics"], ["Graphic Communication", "Visual Arts"],
                    ["History", "Human History"], ["Home Economics — Fashion & Textile Technology", "Visual Arts"], ["Home Economics — Health & Food Technology", "Agriculture"],
                    ["Home Economics — Lifestyle & Consumer Technology", "Family & Consumer Science"], ["Information Systems", "Computer Science"], ["Italian", "Linguistics"],
                    ["Latin", "Linguistics"], ["Managing Environmental Resources", "Organisational Studies"], ["Mathematics", "Mathematics"], ["Mechatronics", "Engineering & Technology"], 
                    ["Media Studies", "Journalism, Media Studies & Communication"], ["Modern Studies", "Anthropology"], ["Music", "Performing Arts"], ["Philosophy", "Philosophy"],
                    ["Physical Education", "Human Physical Performance & Recreation"], ["Physics", "Physics"], ["Politics", "Political Science"], ["Product Design", "Architecture & Design"],
                    ["Psychology", "Psychology"], ["Religious, Moral & Philosophical Studies", "Religious Studies"], ["Russian", "Linguistics"], ["Sociology", "Sociology"],
                    ["Spanish", "Linguistics"], ["Technological Studies", "Computer Science"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = adv_higher
        db.session.add(s)
        db.session.add(q)


    for subject in [["Accounting", "Economics"], ["Administration", "Organisational Studies"], ["Applied Mathematics: Mechanics", "Mathematics"], ["Applied Mathematics: Statistics", "Mathematics"],
                    ["Art & Design Enquiry: Design", "Visual Arts"], ["Art & Design Enquiry: Expressive", "Visual Arts"], ["Art & Design: Research & Appreciation", "Anthropology"],
                    ["Biology", "Biology"], ["Building & Architectural Technology", "Architecture & Design"], ["Business Management", "Business"], ["Chemistry", "Chemistry"],
                    ["Civil Engineering", "Engineering & Technology"], ["Classical Greek", "Linguistics"], ["Classical Studies", "Literature"], ["Computing", "Computer Science"],
                    ["Drama", "Performing Arts"], ["Economics", "Economics"], ["Electronics", "Engineering & Technology"], ["English", "Literature"], ["French", "Linguistics"],
                    ["Gaelic", "Linguistics"], ["Gaidhlig", "Linguistics"], ["Geography", "Geography"], ["Geology", "Geography"], ["German", "Linguistics"], ["Graphic Communication", "Visual Arts"],
                    ["History", "Human History"], ["Home Economics — Fashion & Textile Technology", "Visual Arts"], ["Home Economics — Health & Food Technology", "Agriculture"],
                    ["Home Economics — Lifestyle & Consumer Technology", "Family & Consumer Science"], ["Information Systems", "Computer Science"], ["Italian", "Linguistics"],
                    ["Latin", "Linguistics"], ["Managing Environmental Resources", "Organisational Studies"], ["Mathematics", "Mathematics"], ["Mechatronics", "Engineering & Technology"],
                    ["Media Studies", "Journalism, Media Studies & Communication"], ["Modern Studies", "Anthropology"], ["Music", "Performing Arts"], ["Philosophy", "Philosophy"],
                    ["Physical Education", "Human Physical Performance & Recreation"], ["Physics", "Physics"], ["Politics", "Political Science"], ["Product Design", "Architecture & Design"],
                    ["Psychology", "Psychology"], ["Religious, Moral & Philosophical Studies", "Religious Studies"], ["Russian", "Linguistics"], ["Sociology", "Sociology"],
                    ["Spanish", "Linguistics"], ["Technological Studies", "Computer Science"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = diploma
        db.session.add(s)
        db.session.add(q)


    db.session.commit()

    for subject in [["Accounting & Finance","Economics"], ["Aeronautical & Manufacturing Engineering","Engineering & Technology"], ["Agriculture & Forestry","Agriculture"],
                    ["American Studies","Area Studies"], ["Anatomy & Physiology","Human Physical Performance & Recreation"], ["Anthropology","Anthropology"], ["Archaeology","Archaeology"],
                    ["Architecture","Architecture & Design"], ["Art & Design","Visual Arts"], ["Biological Sciences","Biology"], ["Business & Management Studies","Business"], 
                    ["Celtic Studies","Linguistics"], ["Chemical Engineering","Chemistry"], ["Chemistry","Chemistry"], ["Civil Engineering","Engineering & Technology"],
                    ["Classics & Ancient History","Human History"], ["Communication & Media Studies","Journalism, Media Studies & Communication"], ["Complementary Medicine","Medicine"],
                    ["Computer Science","Computer Science"], ["Counselling","Psychology"], ["Criminology","Law"], ["Dentistry","Medicine"], ["Drama, Dance & Cinematics","Performing Arts"],
                    ["East & South Asian Studies","Area Studies"], ["Economics","Economics"], ["Education","Education"], ["Electrical & Electronic Engineering","Engineering & Technology"],
                    ["English","Literature"], ["Fashion","Visual Arts"], ["Film Making","Performing Arts"], ["Food Science","Agriculture"], ["French","Linguistics"], 
                    ["Geography & Environmental Sciences","Geography"], ["Geology","Earth Sciences"], ["General Engineering","Engineering & Technology"], ["German","Linguistics"], ["History","Human History"],
                    ["History of Art, Architecture & Design","Human History"], ["Hospitality, Leisure, Recreation & Tourism","Sociology"], ["Iberian Languages/Hispanic Studies","Area Studies"],
                    ["Land & Property Management","Environmental Studies"], ["Law","Law"], ["Librarianship & Information Management","Library & Museum Studies"], ["Linguistics","Linguistics"],
                    ["Marketing","Business"], ["Materials Technology","Engineering & Technology"], ["Mathematics","Mathematics"], ["Mechanical Engineering","Engineering & Technology"],
                    ["Medicine","Medicine"], ["Middle Eastern and African Studies","Area Studies"], ["Music","Performing Arts"], ["Nursing","Medicine"], ["Ophthalmics","Medicine"],
                    ["Pharmacology & Pharmacy","Chemistry"], ["Philosophy","Philosophy"], ["Physics and Astronomy","Physics"], ["Physiotherapy","Human Physical Performance & Recreation"],
                    ["Politics","Political Science"], ["Psychology","Psychology"], ["Robotics","Computer Science"], ["Russian & East European Languages","Linguistics"], ["Social Policy","Social Work"],
                    ["Social Work","Social Work"], ["Sociology","Sociology"], ["Sports Science","Human Physical Performance & Recreation"], ["Theology & Religious Studies","Religious Studies"],
                    ["Town & Country Planning and Landscape Design","Architecture & Design"], ["Veterinary Medicine","Medicine"], ["Youth Work","Social Work"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = bachelors_degree
        db.session.add(s)
        db.session.add(q)

    db.session.commit()

    for subject in [["Accounting & Finance","Economics"], ["Aeronautical & Manufacturing Engineering","Engineering & Technology"], ["Agriculture & Forestry","Agriculture"],
                    ["American Studies","Area Studies"], ["Anatomy & Physiology","Human Physical Performance & Recreation"], ["Anthropology","Anthropology"], ["Archaeology","Archaeology"],
                    ["Architecture","Architecture & Design"], ["Art & Design","Visual Arts"], ["Biological Sciences","Biology"], ["Business & Management Studies","Business"],
                    ["Celtic Studies","Linguistics"], ["Chemical Engineering","Chemistry"], ["Chemistry","Chemistry"], ["Civil Engineering","Engineering & Technology"],
                    ["Classics & Ancient History","Human History"], ["Communication & Media Studies","Journalism, Media Studies & Communication"], ["Complementary Medicine","Medicine"],
                    ["Computer Science","Computer Science"], ["Counselling","Psychology"], ["Criminology","Law"], ["Dentistry","Medicine"], ["Drama, Dance & Cinematics","Performing Arts"],
                    ["East & South Asian Studies","Area Studies"], ["Economics","Economics"], ["Education","Education"], ["Electrical & Electronic Engineering","Engineering & Technology"],
                    ["English","Literature"], ["Fashion","Visual Arts"], ["Film Making","Performing Arts"], ["Food Science","Agriculture"], ["French","Linguistics"],
                    ["Geography & Environmental Sciences","Geography"], ["Geology","Earth Sciences"], ["General Engineering","Engineering & Technology"], ["German","Linguistics"], ["History","Human History"],
                    ["History of Art, Architecture & Design","Human History"], ["Hospitality, Leisure, Recreation & Tourism","Sociology"], ["Iberian Languages/Hispanic Studies","Area Studies"],
                    ["Land & Property Management","Environmental Studies"], ["Law","Law"], ["Librarianship & Information Management","Library & Museum Studies"], ["Linguistics","Linguistics"],
                    ["Marketing","Business"], ["Materials Technology","Engineering & Technology"], ["Mathematics","Mathematics"], ["Mechanical Engineering","Engineering & Technology"],
                    ["Medicine","Medicine"], ["Middle Eastern and African Studies","Area Studies"], ["Music","Performing Arts"], ["Nursing","Medicine"], ["Ophthalmics","Medicine"],
                    ["Pharmacology & Pharmacy","Chemistry"], ["Philosophy","Philosophy"], ["Physics and Astronomy","Physics"], ["Physiotherapy","Human Physical Performance & Recreation"],
                    ["Politics","Political Science"], ["Psychology","Psychology"], ["Robotics","Computer Science"], ["Russian & East European Languages","Linguistics"], ["Social Policy","Social Work"],
                    ["Social Work","Social Work"], ["Sociology","Sociology"], ["Sports Science","Human Physical Performance & Recreation"], ["Theology & Religious Studies","Religious Studies"],
                    ["Town & Country Planning and Landscape Design","Architecture & Design"], ["Veterinary Medicine","Medicine"], ["Youth Work","Social Work"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = foundation_degree
        db.session.add(s)
        db.session.add(q)

    db.session.commit()

    for subject in [["Accounting & Finance","Economics"], ["Aeronautical & Manufacturing Engineering","Engineering & Technology"], ["Agriculture & Forestry","Agriculture"],
                    ["American Studies","Area Studies"], ["Anatomy & Physiology","Human Physical Performance & Recreation"], ["Anthropology","Anthropology"], ["Archaeology","Archaeology"],
                    ["Architecture","Architecture & Design"], ["Art & Design","Visual Arts"], ["Biological Sciences","Biology"], ["Business & Management Studies","Business"], 
                    ["Celtic Studies","Linguistics"], ["Chemical Engineering","Chemistry"], ["Chemistry","Chemistry"], ["Civil Engineering","Engineering & Technology"],
                    ["Classics & Ancient History","Human History"], ["Communication & Media Studies","Journalism, Media Studies & Communication"], ["Complementary Medicine","Medicine"],
                    ["Computer Science","Computer Science"], ["Counselling","Psychology"], ["Criminology","Law"], ["Dentistry","Medicine"], ["Drama, Dance & Cinematics","Performing Arts"],
                    ["East & South Asian Studies","Area Studies"], ["Economics","Economics"], ["Education","Education"], ["Electrical & Electronic Engineering","Engineering & Technology"],
                    ["English","Literature"], ["Fashion","Visual Arts"], ["Film Making","Performing Arts"], ["Food Science","Agriculture"], ["French","Linguistics"], 
                    ["Geography & Environmental Sciences","Geography"], ["Geology","Earth Sciences"], ["General Engineering","Engineering & Technology"], ["German","Linguistics"], ["History","Human History"],
                    ["History of Art, Architecture & Design","Human History"], ["Hospitality, Leisure, Recreation & Tourism","Sociology"], ["Iberian Languages/Hispanic Studies","Area Studies"],
                    ["Land & Property Management","Environmental Studies"], ["Law","Law"], ["Librarianship & Information Management","Library & Museum Studies"], ["Linguistics","Linguistics"],
                    ["Marketing","Business"], ["Materials Technology","Engineering & Technology"], ["Mathematics","Mathematics"], ["Mechanical Engineering","Engineering & Technology"],
                    ["Medicine","Medicine"], ["Middle Eastern and African Studies","Area Studies"], ["Music","Performing Arts"], ["Nursing","Medicine"], ["Ophthalmics","Medicine"],
                    ["Pharmacology & Pharmacy","Chemistry"], ["Philosophy","Philosophy"], ["Physics and Astronomy","Physics"], ["Physiotherapy","Human Physical Performance & Recreation"],
                    ["Politics","Political Science"], ["Psychology","Psychology"], ["Robotics","Computer Science"], ["Russian & East European Languages","Linguistics"], ["Social Policy","Social Work"],
                    ["Social Work","Social Work"], ["Sociology","Sociology"], ["Sports Science","Human Physical Performance & Recreation"], ["Theology & Religious Studies","Religious Studies"],
                    ["Town & Country Planning and Landscape Design","Architecture & Design"], ["Veterinary Medicine","Medicine"], ["Youth Work","Social Work"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = masters_degree
        db.session.add(s)
        db.session.add(q)
    
    db.session.commit()

    for subject in [["Accounting & Finance","Economics"], ["Aeronautical & Manufacturing Engineering","Engineering & Technology"], ["Agriculture & Forestry","Agriculture"],
                    ["American Studies","Area Studies"], ["Anatomy & Physiology","Human Physical Performance & Recreation"], ["Anthropology","Anthropology"], ["Archaeology","Archaeology"],
                    ["Architecture","Architecture & Design"], ["Art & Design","Visual Arts"], ["Biological Sciences","Biology"], ["Business & Management Studies","Business"], 
                    ["Celtic Studies","Linguistics"], ["Chemical Engineering","Chemistry"], ["Chemistry","Chemistry"], ["Civil Engineering","Engineering & Technology"],
                    ["Classics & Ancient History","Human History"], ["Communication & Media Studies","Journalism, Media Studies & Communication"], ["Complementary Medicine","Medicine"],
                    ["Computer Science","Computer Science"], ["Counselling","Psychology"], ["Criminology","Law"], ["Dentistry","Medicine"], ["Drama, Dance & Cinematics","Performing Arts"],
                    ["East & South Asian Studies","Area Studies"], ["Economics","Economics"], ["Education","Education"], ["Electrical & Electronic Engineering","Engineering & Technology"],
                    ["English","Literature"], ["Fashion","Visual Arts"], ["Film Making","Performing Arts"], ["Food Science","Agriculture"], ["French","Linguistics"], 
                    ["Geography & Environmental Sciences","Geography"], ["Geology","Earth Sciences"], ["General Engineering","Engineering & Technology"], ["German","Linguistics"], ["History","Human History"],
                    ["History of Art, Architecture & Design","Human History"], ["Hospitality, Leisure, Recreation & Tourism","Sociology"], ["Iberian Languages/Hispanic Studies","Area Studies"],
                    ["Land & Property Management","Environmental Studies"], ["Law","Law"], ["Librarianship & Information Management","Library & Museum Studies"], ["Linguistics","Linguistics"],
                    ["Marketing","Business"], ["Materials Technology","Engineering & Technology"], ["Mathematics","Mathematics"], ["Mechanical Engineering","Engineering & Technology"],
                    ["Medicine","Medicine"], ["Middle Eastern and African Studies","Area Studies"], ["Music","Performing Arts"], ["Nursing","Medicine"], ["Ophthalmics","Medicine"],
                    ["Pharmacology & Pharmacy","Chemistry"], ["Philosophy","Philosophy"], ["Physics and Astronomy","Physics"], ["Physiotherapy","Human Physical Performance & Recreation"],
                    ["Politics","Political Science"], ["Psychology","Psychology"], ["Robotics","Computer Science"], ["Russian & East European Languages","Linguistics"], ["Social Policy","Social Work"],
                    ["Social Work","Social Work"], ["Sociology","Sociology"], ["Sports Science","Human Physical Performance & Recreation"], ["Theology & Religious Studies","Religious Studies"],
                    ["Town & Country Planning and Landscape Design","Architecture & Design"], ["Veterinary Medicine","Medicine"], ["Youth Work","Social Work"]]:

        s = Subject.newSubject(subject[0])
        s.field = Field.newField(subject[1])
        q = Qualification()
        q.subject = s
        q.qualification_type = phd
        db.session.add(s)
        db.session.add(q)

    db.session.commit()


def DefineFields():
    
    l = ["Human History", "Linguistics", "Literature", "Performing Arts", "Visual Arts", "Philosophy", "Religious Studies",
    "Anthropology", "Ethnic & Cultural Studies", "Archaeology", "Area Studies", "Economics", "Gender Studies", "Geography",
    "Organisational Studies", "Political Science", "Psychology", "Sociology", "Biology", "Chemistry", "Physics", "Earth Sciences",
    "Space Science", "Mathematics", "Computer Science", "Systems Science", "Agriculture", "Architecture & Design", "Business",
    "Divinity", "Education", "Engineering & Technology", "Environmental Studies", "Family & Consumer Science",
    "Human Physical Performance & Recreation", "Journalism, Media Studies & Communication", "Law", "Library & Museum Studies",
    "Medicine", "Military Science", "Public Administration", "Social Work", "Transportation"]

    for name in l:
        f = Field()
        f.name = name
        db.session.add(f)

    db.session.commit()

    return len(l)
