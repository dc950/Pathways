from ..models import QualificationType, Qualification, Subject, Field
from .. import db

def Setup():
    DefineFields()
    noQT = DefineQualificationTypes()
    noS = DefineSubjects()
    DefineQualifications()

def DefineQualifications():
    print("Test")

gcse = QualificationType()
higher = QualificationType()
adv_higher = QualificationType()
bachelors_degree = QualificationType()
masters_degree = QualificationType()
phd = QualificationType()

def DefineQualificationTypes():

    QualificationType.query.delete()

    """ 1 Added """
    global gcse
    gcse = QualificationType()
    gcse.name = "GCSE"
    gcse.level = 2
    db.session.add(gcse)

    """ 2 """
    global btec2
    btec2 = QualificationType()
    btec2.name = "BTEC Level 2"
    btec2.level = 2
    db.session.add(btec2)

    """ 3 """
    global a_level
    a_level = QualificationType()
    a_level.name = "A-Level"
    a_level.level = 3
    db.session.add(a_level)

    """ 4 """
    global btec3
    btec3 = QualificationType()
    btec3.name = "BTEC Level 3"
    btec3.level = 3
    db.session.add(btec3)

    """ 5 Added """
    global higher
    higher = QualificationType()
    higher.name = "Scottish Higher"
    higher.level = 3
    db.session.add(higher)

    """ 6 """
    global btec4
    btec4 = QualificationType()
    btec4.name = "BTEC Level 4"
    btec4.level = 4
    db.session.add(btec4)

    """ 7 """
    global cert_higher_ed
    cert_higher_ed = QualificationType()
    cert_higher_ed.name = "Certificate of Higher Education"
    cert_higher_ed.level = 4
    db.session.add(cert_higher_ed)

    """ 8 Added """
    global adv_higher
    adv_higher = QualificationType()
    adv_higher.name = "Scottish Advanced Higher"
    adv_higher.level = 4
    db.session.add(adv_higher)

    """ 9 """
    global diploma
    diploma = QualificationType()
    diploma.name = "Diploma"
    diploma.level = 4
    db.session.add(diploma)

    """ 10 """
    global btec5
    btec5 = QualificationType()
    btec5.name = "BTEC Level 5"
    btec5.level = 5
    db.session.add(btec5)

    """ 11 """
    global foundation_degree
    foundation_degree = QualificationType()
    foundation_degree.name = "Foundation Degree"
    foundation_degree.level = 5
    db.session.add(foundation_degree)

    """ 12 """
    global bachelors_degree
    bachelors_degree = QualificationType()
    bachelors_degree.name = "Bachelor's Degree"
    bachelors_degree.level = 6
    db.session.add(bachelors_degree)

    """ 13 """
    global masters_degree
    masters_degree = QualificationType()
    masters_degree.name = "Master's Degree"
    masters_degree.level = 7
    db.session.add(masters_degree)

    """ 14 """
    global phd
    phd = QualificationType()
    phd.name = "PhD"
    phd.level = 8
    db.session.add(phd)

    db.session.commit()

def DefineSubjects():

    Subject.query.delete()
#    Qualification.query.delete()

    for name in ["English", "English Language", "English Lit", "Mathematics", "Welsh", "Welsh Second Language","Welsh Language",
                 "Irish", "Science", "Biology", "Chemistry", "Physics", "Core Science", "Double Science", "Triple Science",
                 "Additional Science",

                 "Afrikaans", "Arabic", "Bengali", "Cantonese", "Mandarin", "Dutch", "French", "Applied French",
                 "Business French", "German", "Applied German", "Business German", "Modern Greek", "Gujarati", "Modern Hebrew", "Hindi",
                 "Gaeilge", "Italian", "Japanese", "Maltese", "Malay", "Manx", "Punjabi", "Persian", "Polish", "Portuguese", "Russian",
                 "Somali", "Spanish", "Tamil", "Telugu", "Turkish", "Urdu", "Yoruba",

                 "Classical Tamil", "Classical Arabic", "Classical Greek", "Biblical Hebrew", "Latin", "Classical Sanskrit",

                 "Design & Technology", "Parametric CAD", "Electronic Products", "Electronics", "Food Technology", "Graphic Design/Products",
                 "Product Design", "Resistant Materials", "Textiles", "Product Design", "Resistant Materials", "Textiles", "Systems & Control",
                 "Catering", "Electronics with Resistant Materials", "Engineering", "Engineering & Manufacturing", "Home Economics",
                 "Food & Nutrition", "Child Development", "Textiles", "Manufacturing", "ICT", "Computer Science", "Computing",
                 "Digital technology",

                 "Citizenship", "Classical Civilisation", "Economics", "Geography", "History", "Humanities", "Religious Studies", "Buddhism",
                 "Christianity", "Hinduism", "Islam", "Judaism", "Philosophy & Ethics", "Sikhism",

                 "Business Studies", "Applied Business", "Business & Economics", "Business & Communications Systems", "Financial Services",
                 "Health & Social Care", "Hospitality", "Law", "Leisure & Tourism", "Psychology", "Sociology", "Travel & Tourism",

                 "Animation", "Applied Art & Design", "Art & Design", "Fine Art", "Graphics", "Photography", "Textiles", "3D Design", "Dance",
                 "Drama", "Digital Photography", "Expressive Arts", "Film Studies", "Media Studies", "Moving Image Arts", "Music",
                 "Performing Arts", "Original Writing",

                 "Accounting", "Additional Mathematics", "Astronomy", "Construction", "Construction & the Built Environment",
                 "Environmental Science", "Geology", "General Studies", "Human Physiology & Health", "IFS Personal Finance", "Journalism",
                 "Learning for Life & Work", "Motorsport", "Motor Vehicle & Road User Studies", "Personal & Social Education",
                 "Physical Education", "Preparation for Working Life", "Rural & Agricultural Science", "Statistics"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        q.qualification_type = gcse
        db.session.add(s)
        db.session.add(q)

    for name in ["Accounting", "Administration", "Architectural Technology", "Art & Design", "Automotive Engineering", "Biology",
                 "Biotechnology", "Building & Architectural Technology", "Building Services", "Business Management", "Care", "Chemistry",
                 "Civil Engineering", "Classical Greek", "Classical Studies", "Chinese Language & Culture", "Computing", "Construction",
                 "Dance", "Drama", "Early Education & Childcare", "Early Years Care & Education", "Economics", "Electrical Engineering",
                 "Electronics", "English", "English for Speakers of Other Languages", "Fabrication & Welding Engineering", "French", "Gaelic",
                 "Gàidhlig", "Geography", "Geology", "German", "Graphic Communication", "History",
                 "Home Economics: Fashion & Textile Technology", "Home Economics: Health & Food Technology",
                 "Home Economics: Lifestyle & Consumer Technology", "Hospitality: Food & Drink Service", "Hospitality: Professional Cookery",
                 "Hospitality: Reception & Accommodation Operations", "Human Biology", "Information Systems", "Italian", "Land Use", "Latin",
                 "Managing Environmental Resources", "Mandarin Chinese", "Manufacturing", "Mathematics", "Mechanical Engineering",
                 "Mechatronics", "Media Studies", "Modern Studies", "Music", "Personal & Social Education", "Philosophy", "Photography",
                 "Physical Education", "Physics", "Politics", "Product Design", "Psychology", "Religious Education",
                 "Religious, Moral & Philosophical Studies", "Russian", "Sociology", "Spanish", "Technological Studies", "Travel & Tourism",
                 "Urdu"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        s.qualification_type = higher
        db.session.add(s)
        db.session.add(q)

    for name in ["Accounting", "Administration", "Applied Mathematics: Mechanics", "Applied Mathematics: Statistics",
                 "Art & Design Enquiry: Design", "Art & Design Enquiry: Expressive", "Art & Design: Research & Appreciation", "Biology",
                 "Building & Architectural Technology", "Business Management", "Chemistry", "Civil Engineering", "Classical Greek",
                 "Classical Studies", "Computing", "Drama", "Economics", "Electronics", "English", "French", "Gaelic", "Gaidhlig", "Geography",
                 "Geology", "German", "Graphic Communication", "History", "Home Economics — Fashion & Textile Technology",
                 "Home Economics — Health & Food Technology", "Home Economics — Lifestyle & Consumer Technology", "Information Systems",
                 "Italian", "Latin", "Managing Environmental Resources", "Mathematics", "Mechatronics", "Media Studies", "Modern Studies",
                 "Music", "Philosophy", "Physical Education", "Physics", "Politics", "Product Design", "Psychology",
                 "Religious, Moral & Philosophical Studies", "Russian", "Sociology", "Spanish", "Technological Studies"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        s.qualification_type = adv_higher
        db.session.add(s)
        db.session.add(q)

    for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
                 "Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        s.qualification_type = bachelors_degree
        db.session.add(s)
        db.session.add(q)

    for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
                 "Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        s.qualification_type = masters_degree
        db.session.add(s)
        db.session.add(q)

    for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
                 "Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

        s = Subject.newSubject(name)
        q = Qualification()
        q.subject = s
        s.qualification_type = phd
        db.session.add(s)
        db.session.add(q)

    db.session.commit()

def DefineFields():
    Field.query.delete()

    l = ["Human History", "Linguistics", "Literature", "Performing Arts", "Visual Arts", "Philosophy", "Religious Studies",
    "Anthropology", "Ethnic & Cultural Studies", "Archaeology", "Area Studies", "Economics", "Gender Studies", "Geography",
    "Organisational Studies", "Political Science", "Psychology", "Sociology", "Biology", "Chemistry", "Physics", "Earth Sciences",
    "Space Science", "Mathematics", "Computer Science", "Systems Science", "Agiculture", "Architecture & Design", "Business",
    "Divinity", "Education", "Engineering & Technology", "Environmental Studies", "Family & Consumer Science",
    "Human Physical Performance & Recreation", "Journalism, Media Studies & Communication", "Law", "Library & Museum Studies",
    "Medicine", "Military Science", "Public Administration", "Social Work", "Transportation"]

    for name in l:
        f = Field()
        f.name = name
        db.session.add(f)

    db.session.commit()

    return len(l)
