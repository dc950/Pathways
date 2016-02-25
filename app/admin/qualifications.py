from ..models import QualificationType, Qualification
from .. import db

def qualifications():
	print("***** This is a test *****")

	QualificationType.query.delete()

	""" 1 Added """
	qt = QualificationType()
	qt.name = "GCSE"
	qt.level = 2
	db.session.add(qt)

	""" 2 """
	qt = QualificationType()
	qt.name = "BTEC Level 2"
	qt.level = 2
	db.session.add(qt)

	""" 3 """
	qt = QualificationType()
	qt.name = "A-Level"
	qt.level = 3
	db.session.add(qt)

	""" 4 """
	qt = QualificationType()
	qt.name = "BTEC Level 3"
	qt.level = 3
	db.session.add(qt)

	""" 5 Added """
	qt = QualificationType()
	qt.name = "Scottish Higher"
	qt.level = 3
	db.session.add(qt)

	""" 6 """
	qt = QualificationType()
	qt.name = "BTEC Level 4"
	qt.level = 4
	db.session.add(qt)

	""" 7 """
	qt = QualificationType()
	qt.name = "Certificate of Higher Education"
	qt.level = 4
	db.session.add(qt)

	""" 8 Added """
	qt = QualificationType()
	qt.name = "Scottish Advanced Higher"
	qt.level = 4
	db.session.add(qt)

	""" 9 """
	qt = QualificationType()
	qt.name = "Diploma"
	qt.level = 4
	db.session.add(qt)

	""" 10 """
	qt = QualificationType()
	qt.name = "BTEC Level 5"
	qt.level = 5
	db.session.add(qt)

	""" 11 """
	qt = QualificationType()
	qt.name = "Foundation Degree"
	qt.level = 5
	db.session.add(qt)

	""" 12 """
	qt = QualificationType()
	qt.name = "Bachelor's Degree"
	qt.level = 6
	db.session.add(qt)

	""" 13 """
	qt = QualificationType()
	qt.name = "Master's Degree"
	qt.level = 7
	db.session.add(qt)

	""" 14 """
	qt = QualificationType()
	qt.name = "PhD"
	qt.level = 8
	db.session.add(qt)

	db.session.commit()

def subjects():

	Qualification.query.delete()

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

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 1
		db.session.add(s)

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

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 5
		db.session.add(s)

	for name in ["Accounting", "Administration", "Applied Mathematics: Mechanics", "Applied Mathematics: Statistics",
	"Art & Design Enquiry: Design", "Art & Design Enquiry: Expressive", "Art & Design: Research & Appreciation", "Biology",
	"Building & Architectural Technology", "Business Management", "Chemistry", "Civil Engineering", "Classical Greek",
	"Classical Studies", "Computing", "Drama", "Economics", "Electronics", "English", "French", "Gaelic", "Gaidhlig", "Geography",
	"Geology", "German", "Graphic Communication", "History", "Home Economics — Fashion & Textile Technology",
	"Home Economics — Health & Food Technology", "Home Economics — Lifestyle & Consumer Technology", "Information Systems",
	"Italian", "Latin", "Managing Environmental Resources", "Mathematics", "Mechatronics", "Media Studies", "Modern Studies",
	"Music", "Philosophy", "Physical Education", "Physics", "Politics", "Product Design", "Psychology",
	"Religious, Moral & Philosophical Studies", "Russian", "Sociology", "Spanish", "Technological Studies"]:

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 8
		db.session.add(s)

	for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
	"Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 12
		db.session.add(s)

	for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
	"Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 13
		db.session.add(s)

	for name in ["Histroy", "Biological Sciences", "Nursing", "Primary Education", "Psychology", "Computer Science", "Sociology",
	"Social Studies", "Computer Systems", "Information Systems", "Maths", "Law", "Business Studies"]:

		s = Qualification()
		s.course_name = name
		s.qualification_type_id = 14
		db.session.add(s)

	db.session.commit()
