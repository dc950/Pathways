from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo



class adminForm(Form):
    submit = SubmitField('Load webcrawler into database')

class qualTypesForm(Form):
    submit = SubmitField('Load Qual Types')

class adminDeleteUser(Form):
    usernamedelete = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Delete User')

class adminWarningEmail(Form):
    usernamewarning = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    submit2 = SubmitField('Send Warning Email')

class deleteAccountForm(Form):
    submit = SubmitField('Delete Account')

