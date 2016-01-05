from app import db
from flask import current_app, flash
from .email import send_email
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_skills = db.Table('user_skills',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('skill_id', db.Integer, db.ForeignKey('skills.id')))

'''

user_qualifications = db.Table('user_qualifications',
                               db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                               db.Column('qualification_id', db.Integer, db.ForeignKey('qualifications.id')),
                               db.Column('grade', db.String(1)))

'''


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(26), index=True)
    last_name = db.Column(db.String(26), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), unique=True)

    skills = db.relationship("Skill", secondary=user_skills)
    qualifications = db.relationship('UserQualification', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.first_name + self.last_name)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def send_confirmation_email(self):
        token = self.generate_confirmation_token()
        send_email(self.email, 'Confirm Your Account', 'auth/email/confirm', user=self, token=token)
        flash('A confirmation email has been sent to your email')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_username(self):
        u_name = (self.first_name + self.last_name).lower()
        if User.query.filter_by(username=u_name).first() is None:
            self.username = u_name
            return
        version = 1
        while True:
            new_u_name = (u_name + str(version)).lower()
            if User.query.filter_by(username=new_u_name).first() is None:
                self.username = new_u_name
                return
            version += 1

    def add_skill(self, skill):
        """
        Adds the skill to the user
        :param skill: The skill object to be added
        """
        if skill not in self.skills:
            self.skills.append(skill)

    def add_skill_name(self, skill_name):
        """
        Adds the skill to the user by name - if the skill does not exist, it is created
        :param skill_name: the name of the skill to be added
        """
        s = Skill.query.filter_by(name=skill_name)
        if s.count():
            if s.first() not in self.skills:
                self.skills.append(s.first())
        else:
            s = Skill(name=skill_name)
            db.session.add(s)
            db.session.commit()
            self.skills.append(s)


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Skill %r>' % self.name


class Qualification(db.Model):
    __tablename__ = 'qualifications'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(128))
    qualification_type_id = db.Column(db.Integer, db.ForeignKey('qualification_types.id'))
    qualification_type = db.relationship("QualificationType")

    @property
    def level(self):
        if self.qualification_type is None:
            raise AttributeError('This Qualification has no QualificationType')
        else:
            return self.qualification_type.level

    @property
    def qualification_name(self):
        if self.qualification_type is None:
            raise AttributeError('This Qualification has no QualificationType')
        else:
            return self.qualification_type.name

    def __repr__(self):
        return '<Qualification %r>' % (self.level + self.name)


class QualificationType(db.Model):
    __tablename__ = 'qualification_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    level = db.Column(db.Integer)


class UserQualification(db.Model):
    __tablename__ = 'user_qualifications'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    qualifications_id = db.Column(db.Integer, db.ForeignKey('qualifications.id'), primary_key=True)
    grade = db.Column(db.String(1))  # There's probably a better way to do this...
    qualification = db.relationship("Qualification")

    @property
    def course_name(self):
        return self.qualification.course_name

    @property
    def qualification_name(self):
        return self.qualification.qualification_name

    @property
    def level(self):
        return self.qualification.level
