from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FieldList
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import Field


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


class adminCustomEmailForm(Form):
    usernamecustom = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    customeemailbox = TextAreaField('Write the body of the email here:', validators=[DataRequired()])
    submit3 = SubmitField('Send Custom Email')


# class SetField(Form):
#     # fields = FieldList(SelectField('eg'))
#     fields = FieldList(SelectField('course', choices=[]))
#     submit = SubmitField('Submit')
#
#     def __init__(self, **kwargs):
#         super(SetField, self).__init__(**kwargs)
#
#         all_fields_choices = sorted([(x.id, x.name) for x in Field.query.all()], key=lambda z: z[1])
#         all_fields_choices.insert(0, (-1, 'None'))
#         self.fields.unbound_field.choices = all_fields_choices
#

