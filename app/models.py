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


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(26), index=True)
    last_name = db.Column(db.String(26), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), unique=True)

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
