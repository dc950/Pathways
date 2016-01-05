import unittest
from app.models import User, Skill
from app import db, create_app


class SkillsModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_relationship(self):
        s = Skill(name="pyhton")
        u = User()
        u.skills.append(s)
        db.session.add(s)
        db.session.add(u)
        db.session.commit()
        self.assertEqual(s, u.skills[0])

    def test_add_skills(self):
        s = Skill(name="css")
        u = User()
        db.session.add(s)
        db.session.add(u)
        db.session.commit()
        u.add_skill(s)
        self.assertEqual(s, u.skills[0])

    def test_add_existing_skills_by_name(self):
        s = Skill(name="php")
        u = User()
        db.session.add(s)
        db.session.add(u)
        db.session.commit()
        u.add_skill_name("php")
        db.session.add(u)
        db.session.commit()
        self.assertEqual(s, u.skills[0])

    def test_add_non_existant_skills_by_name(self):
        u = User()
        db.session.add(u)
        db.session.commit()
        u.add_skill_name("html")
        s = Skill.query.filter_by(name="html")
        print(s.count)
        self.assertTrue(s.count() > 0)
        self.assertEqual(s.first(), u.skills[0])
