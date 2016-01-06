import unittest
from app.models import User, Qualification, QualificationType, Career, CareerQualification
from app import db, create_app


class CareerModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_qualification_relationship(self):
        qt = QualificationType(name="Higher", level=6)
        q = Qualification(course_name="Computing", qualification_type=qt)
        c = Career(name="Web Developer", description="Worst job ever")
        c.add_qualification(q, 5)
        self.assertEqual(c.qualifications[0].course_name, "Computing")
        self.assertEqual(c.qualifications[0].points, 5)
