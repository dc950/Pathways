from app import db
from flask import current_app, flash, request
from .email import send_email
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager
from hashlib import md5
from datetime import datetime


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
    profile_comments = db.relationship('Comment', backref='profile', foreign_keys="[Comment.profile_id]", lazy='dynamic')
    authored_comments = db.relationship('Comment', backref='author', foreign_keys="[Comment.author_id]", lazy='dynamic')

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

    def gravatar(self, size=128):
        if request.is_secure:
            url = 'https://www.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if not self.avatar_hash:
            self.avatar_hash = md5(self.email.encode('utf-8')).hexdigest()

        final_url = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                url=url, hash=self.avatar_hash, size=size, default=self.def_avatar, rating='g')
        if not self.can(Permission.HAVE_AVATAR):
            # If the user is not permitted to have an avatar, we force the default type
            # For some reason setting f=n does not work, so need to separately append
            final_url += '&f=y'
            print("user cannot have normal avatar")
        return final_url

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

    def send_new_delete_acc_email(self):
        token = self.generate_delete_account_token()
        send_email(self.email, 'To delete your account', 'auth/email/delete-account', user=self, token=token)
        flash('A confirmation email has been sent to your email')

    def generate_new_password_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'new_password': self.id})

    def generate_delete_account_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'delete_account': self.id})

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

    def remove_permission(self, permission):
        user = Role.query.filter_by(name='User').first()
        print(user)
        print(self.role)
        restricted = Role.query.filter_by(name='Restricted').first()
        no_comment = Role.query.filter_by(name='NoComment').first()
        no_avatar = Role.query.filter_by(name='NoAvatar').first()

        if self.role == no_comment:
            if permission == Permission.HAVE_AVATAR:
                self.role = restricted
        elif self.role == no_avatar:
            if permission == Permission.MAKE_COMMENT:
                self.role = restricted
        elif self.role == user:
            print("role is user")
            if permission == Permission.HAVE_AVATAR:
                self.role = no_avatar
            elif permission == Permission.MAKE_COMMENT:
                self.role = no_comment


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

    @property
    def unseen_comments(self):
        comments = Comment.query.filter_by(profile=self).filter_by(seen=False).all()
        return comments



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
    subjects = db.relationship('CareerSubject', lazy='dynamic')
    skills = db.relationship('CareerSkill', lazy='dynamic')
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
    field = db.relationship("Field", backref='subjects')

    def __repr__(self):
        return '<Career %r>' % self.name

    def add_subject(self, subject, points=1):
        """
        Adds the subject to the career
        :param subject: the subject object of the subject to be added
        :param points: The points for the qualification with relation to how important it is for the career
        """

        if subject in self.subjects:
            # Subject already assigned
            return

        cs = CareerSubject(subject=subject)
        if points:
            cs.points = points
        self.subjects.append(cs)

    def add_subject_name(self, subject_name, points=1):
        """
        Adds the subject to the career when given the name
        :param subject: the string name of the subject to be added
        :param points: The points for the qualification with relation to how important it is for the career
        """

        #Find if the subject exists:
        subject_query = Subject.query.filter_by(name=subject_name).first()
        subject = None
        if subject_query is None:
            subject = Subject(name=subject_name)
        else:
            subject = subject_query

        if subject in self.subjects:
            # Subject already assigned
            return

        cs = CareerSubject(subject=subject)
        if points:
            cs.points = points
        self.subjects.append(cs)

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


class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    # interests and skills?


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
    field = db.relationship("Field", backref='subjects')

    @staticmethod
    def newSubject(name):
        """
        Will return a new subject or if one already exists, it will return that one
        :param name: The name of the subject
        :return: A subject object with that name to be used.
        """
        subject = Subject.query.filter_by(name=name).first()
        if subject:
            return subject
        else:
            return Subject(name=name)

# class UniQualification(db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     qualification_type_id = db.Column(db.Integer, db.ForeignKey('qualification_types.id'))
#     qualification_type = db.relationship("QualificationType")


class Qualification(db.Model):
    __tablename__ = 'qualifications'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref='qualifications')
    qualification_type_id = db.Column(db.Integer, db.ForeignKey('qualification_types.id'))
    qualification_type = db.relationship("QualificationType")
    maxucaspoints = db.Column(db.String(1024))
    minucaspoints = db.Column(db.String(1024))
    alevelgrades = db.Column(db.String(1024))
    highers = db.Column(db.String(1024))
    internationalbaccalaureate = db.Column(db.String(1024))
    advancedhighers = db.Column(db.String(1024))

    @property
    def name(self):
        if self.subject is None:
            raise AttributeError('This Qualification has no related Subject')
        else:
            return self.subject.name

    @property
    def field(self):
        if self.subject is None:
            raise AttributeError('This Qualification has no related Subject')
        else:
            return self.subject.field.name

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

    @staticmethod
    def filter_name_type(name, qualification_type):
        subject = Subject.query.filter_by(name=name).first()
        return Qualification.query.filter_by(subject=subject).filter_by(qualification_type=qualification_type)

    def __repr__(self):
        return self.name


class QualificationType(db.Model):
    __tablename__ = 'qualification_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    level = db.Column(db.Integer)
    ucas_points = db.Column(db.Integer)

    @staticmethod
    def newType(name):
        """
        Will return a new subject or if one already exists, it will return that one
        :param name: The name of the subject
        :return: A subject object with that name to be used.
        """
        type = QualificationType.query.filter_by(name=name).first()
        if type:
            return type
        else:
            return QualificationType(name=name)



class UserQualification(db.Model):
    __tablename__ = 'user_qualifications'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    qualifications_id = db.Column(db.Integer, db.ForeignKey('qualifications.id'), primary_key=True)
    grade = db.Column(db.String(1))  # There's probably a better way to do this...
    qualification = db.relationship("Qualification")

    @property
    def name(self):
        return self.qualification.name

    @property
    def qualification_name(self):
        return self.qualification.qualification_name

    @property
    def level(self):
        return self.qualification.level


class CareerSubject(db.Model):
    __tablename__ = 'career_subjects'
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
    points = db.Column(db.Integer)
    subject = db.relationship("Subject")

    @property
    def name(self):
        return self.subject.name


class CareerSkill(db.Model):
    __tablename__ = 'career_skills'
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), primary_key=True)
    skills_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    points = db.Column(db.Integer)
    skill = db.relationship("Skill")

    @property
    def name(self):
        return self.skill.name

# class UniCourses(Qualification):
#     __tablename__= 'unicourses'
#     ucaspoints = db.Column(db.String(1024))
#     alevelgrades = db.Column(db.String(1024))
#     highers = db.Column(db.String(1024))
#     internationalbaccalaureate = db.Column(db.String(1024))
#     advancedhighers = db.Column(db.String(1024))
#
#     def __repr__(self):
#         return '<UniCourses %r>' % self.coursename


class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    profile_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seen = db.Column(db.Boolean, default=False)

    @staticmethod
    def add_comment(author, profile, body):
        """
        Writes a comment on a users profile
        :param author: THe user making the comment
        :param profile: The user who's page is being commented on
        :param body: The body of the text
        :return: The comment
        """
        # Do some checks to make sure things are allowed regarding privacy, do a flash to show it didn't work etc.
        comment = Comment(body=body, author_id=author.id, profile_id=profile.id)
        db.session.add(comment)


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
            'Restricted': (0x00, False),
            'NoComment': (Permission.HAVE_AVATAR, False),
            'NoAvatar': (Permission.MAKE_COMMENT, False),
            'User': (Permission.MAKE_COMMENT |
                     Permission.HAVE_AVATAR, True),
            'Mentor': (Permission.MAKE_COMMENT |
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
    MAKE_COMMENT = 0x02
    MENTOR = 0x04
    MODERATE_CONTENT = 0x08
    ADMINISTER = 0x80
