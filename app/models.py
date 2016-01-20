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

# If a request is made a connection is added.
# If a request is sent, it is added again the other way around.  If both exist, the connection is made...
connections = db.Table('connections',
                       db.Column('requesting_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('invitation_id', db.Integer, db.ForeignKey('users.id')))


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

    connection_requests = db.relationship('User',
                                          secondary=connections,
                                          primaryjoin=(connections.c.requesting_id == id),
                                          secondaryjoin=(connections.c.invitation_id == id),
                                          backref=db.backref('connection_invitations', lazy='dynamic'),
                                          lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.first_name + self.last_name)

    @property
    def connections(self):
        cons = []
        for c in self.connection_requests:
            if self in c.connection_requests:
                cons.append(c)
        return cons

    @property
    def invitations(self):
        invs = []
        for i in self.connection_invitations:
            if i not in self.connections:
                invs.append(i)
        return invs

    @property
    def requests(self):
        reqs = []
        for r in self.connection_requests:
            if r not in self.connections:
                reqs.append(r)
        return reqs

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    def made_request(self, user):
        return user in self.connection_requests

    def send_request(self, user):
        """
        Sends a request TO this user FROM the user in the parameter
        :param user: the user sending the request
        """
        user.connection_requests.append(self)

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=86400000):
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
            self.add_skill(s.first())
        else:
            s = Skill(name=skill_name)
            db.session.add(s)
            db.session.commit()
            self.add_skill(s)

    def add_qualification(self, qualification, grade=None):
        """
        Adds the qualification to the user
        :param qualification: the Qualification object to be added
        :param grade: The grade for the qualification
        """
        uq = UserQualification()
        uq.qualification = qualification
        if grade:
            uq.grade = grade
        self.qualifications.append(uq)


class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(1024))
    #  Salary Information
    qualifications = db.relationship('CareerQualification', lazy='dynamic')
    skills = db.relationship('CareerSkill', lazy='dynamic')

    def __repr__(self):
        return '<Career %r>' % self.name

    def add_qualification(self, qualification, points=1):
        """
        Adds the qualification to the career
        :param qualification: the Qualification object to be added
        :param points: The points for the qualification with relation to how important it is for the career
        """
        cq = CareerQualification()
        cq.qualification = qualification
        if points:
            cq.points = points
        self.qualifications.append(cq)

    def add_skill(self, skill, points=1):
        """
        Adds the skill to the user
        :param skill: The skill object to be added
        :param points: The points for showing the importance of the skill
        """
        for c_skill in self.skills:
            if c_skill.skill is skill:
                return
        c_skill = CareerSkill(skill=skill, points=points)
        self.skills.append(c_skill)

    def add_skill_name(self, skill_name, points=1):
        """
        Adds the skill to the user by name - if the skill does not exist, it is created
        :param skill_name: the name of the skill to be added
        :param points: The points for showing the importance of the skill
        """
        s = Skill.query.filter_by(name=skill_name)
        if s.count():
            self.add_skill(s.first(), points)
        else:
            s = Skill(name=skill_name)
            db.session.add(s)
            db.session.commit()
            self.add_skill(s, points)


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


class CareerQualification(db.Model):
    __tablename__ = 'career_qualifications'
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), primary_key=True)
    qualifications_id = db.Column(db.Integer, db.ForeignKey('qualifications.id'), primary_key=True)
    points = db.Column(db.Integer)
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


class CareerSkill(db.Model):
    __tablename__ = 'career_skills'
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), primary_key=True)
    skills_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    points = db.Column(db.Integer)
    skill = db.relationship("Skill")

    @property
    def name(self):
        return self.skill.name
