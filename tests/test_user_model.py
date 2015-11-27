import unittest
from app.models import User
from app import db, create_app


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_username_generation(self):
        u = User(first_name='John', last_name='Doe')
        u.generate_username()
        db.session.add(u)
        db.session.commit()

        u1 = User(first_name='John', last_name='Doe')
        u1.generate_username()
        db.session.add(u1)
        db.session.commit()

        u2 = User(first_name='John', last_name='Doe')
        u2.generate_username()
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u.username, 'johndoe')
        self.assertEqual(u1.username, 'johndoe1')
        self.assertEqual(u2.username, 'johndoe2')
