import unittest
from app.models import User, Qualification, QualificationType, Career, CareerQualification, Skill, Subject
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
        s = Subject(name="Computing")
        q = Qualification(subject=s, qualification_type=qt)
        c = Career(name="Web Developer", description="Worst job ever")
        c.add_qualification(q, 5)
        self.assertEqual(c.qualifications[0].name, "Computing")
        self.assertEqual(c.qualifications[0].points, 5)

    def test_add_skills(self):
        s = Skill(name="css")
        c = Career()
        db.session.add(s)
        db.session.add(c)
        db.session.commit()
        c.add_skill(s, 3)
        self.assertEqual(s, c.skills[0].skill)
        self.assertEqual(c.skills[0].points, 3)

    def test_add_existing_skills_by_name(self):
        s = Skill(name="php")
        c = Career()
        db.session.add(s)
        db.session.add(c)
        db.session.commit()
        c.add_skill_name("php", 2)
        db.session.add(c)
        db.session.commit()
        self.assertEqual(s, c.skills[0].skill)
        self.assertEqual(c.skills[0].points, 2)

    def test_add_non_existant_skills_by_name(self):
        c = Career()
        db.session.add(c)
        db.session.commit()
        c.add_skill_name("html", 4)
        s = Skill.query.filter_by(name="html")
        self.assertTrue(s.count() > 0)
        self.assertEqual(s.first(), c.skills[0].skill)
        self.assertEqual(s.first().name, c.skills[0].name)
        self.assertEqual(c.skills[0].points, 4)
