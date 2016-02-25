from app import db
from flask import current_app, flash, request
from .email import send_email
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager
from hashlib import md5


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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_hash = db.Column(db.String(32))
    def_avatar = db.Column(db.String(16), default='identicon')

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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['PATHWAYS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
                self.confirmed = True
            else:
                self.role = Role.query.filter_by(default=True).first()

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

    def gravatar(self, size=128, rating='g'):
        if request.is_secure:
            url = 'https://www.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if not self.avatar_hash:
            self.avatar_hash = md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                url=url, hash=self.avatar_hash, size=size, default=self.def_avatar, rating=rating)

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

    def generate_confirmation_token(self, expiration=86400):
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

    def send_new_password_email(self):
        token = self.generate_new_password_token()
        send_email(self.email, 'Change your password', 'auth/email/change-password', user=self, token=token)
        flash('A confirmation email has been sent to your email')

    def generate_new_password_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'new_password': self.id})

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

    # SKILLS AND QUALIFICATIONS
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

    # PERMISSIONS
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        fout = open('fake_users.txt', 'w')
        seed()
        for i in range(count):
            email = forgery_py.internet.email_address()
            password = forgery_py.lorem_ipsum.word()
            u = User(email=email,
                     first_name=forgery_py.name.first_name(),
                     last_name=forgery_py.name.last_name(),
                     password=password,
                     confirmed=True)
            u.generate_username()
            db.session.add(u)
            try:
                db.session.commit()
                print((email + " : " + password), file=fout)
            except IntegrityError:
                db.session.rollback()


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
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
        return self.course_name


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

class UniCourses(Qualification):
    __tablename__= 'unicourses'
    ucaspoints = db.Column(db.String(1024))
    alevelgrades = db.Column(db.String(1024))
    highers = db.Column(db.String(1024))
    internationalbaccalaureate = db.Column(db.String(1024))
    advancedhighers = db.Column(db.String(1024))

    def __repr__(self):
        return '<UniCourses %r>' % self.coursename

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.ADD_USERS |
                     Permission.HAVE_AVATAR, True),
            'Mentor': (Permission.ADD_USERS |
                       Permission.HAVE_AVATAR |
                       Permission.MENTOR |
                       Permission.MODERATE_CONTENT, False),
            'Admin': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    HAVE_AVATAR = 0x01
    ADD_USERS = 0x02
    MENTOR = 0x04
    MODERATE_CONTENT = 0x08
    ADMINISTER = 0x80
