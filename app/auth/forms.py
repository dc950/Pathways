from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(1, 64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'), Length(6, 32)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 32)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use')


class ChangePasswordForm(Form):
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'), Length(6, 32)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 32)])
    submit = SubmitField('Change Password')

class DeleteAccountForm(Form):
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Delete Account')

class ForgottenPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Confirm')
