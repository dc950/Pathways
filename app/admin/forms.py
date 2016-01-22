from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError



class adminForm(Form):
    submit = SubmitField('Load webcrawler into database')