import unittest
from app.models import User, Qualification, QualificationType, UserQualification, Subject, Field
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
        f = Field(name="IT")
        s = Subject(name="Computing", field=f)
        q = Qualification(subject=s, qualification_type=t)
        u = User()
        uq = UserQualification(grade="A", qualification=q)
        u.qualifications.append(uq)
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.qualifications[0].qualification_name, "Higher")
        self.assertEqual(u.qualifications[0].name, "Computing")
        self.assertEqual(u.qualifications[0].level, 6)
        self.assertEqual(u.qualifications[0].grade, "A")
        a = Qualification.filter_name_type("Computing", t).first()
        self.assertEqual(a.qualification_name, "Higher")

    def test_add_qualification(self):
        t = QualificationType(name="Higher", level=6)
        s = Subject(name="Computing")
        q = Qualification(subject=s, qualification_type=t)
        u = User()
        u.add_qualification(q, "A")
        self.assertEqual(u.qualifications[0].grade, "A")
        self.assertEqual(u.qualifications[0].name, "Computing")
