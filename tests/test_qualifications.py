import unittest
from app.models import User, Qualification, QualificationType, UserQualification
from app import db, create_app


class QualificationModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_types(self):
        t = QualificationType(name="Higher", level=6)
        q = Qualification(course_name="Computing", qualification_type=t)
        u = User()
        uq = UserQualification(grade="A")
        uq.qualification = q
        u.qualifications.append(uq)
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.qualifications[0].qualification_name, "Higher")
        self.assertEqual(u.qualifications[0].course_name, "Computing")
        self.assertEqual(u.qualifications[0].level, 6)
        self.assertEqual(u.qualifications[0].grade, "A")
        a = u.qualifications.filter(Qualification.course_name == "Computing")
        self.assertEqual(a.first().qualification_name, "Higher")
