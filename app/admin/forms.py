from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AdminForm(Form):
    submit = SubmitField('Load webcrawler into database')


class QualTypesForm(Form):
    submit = SubmitField('Load Qual Types')


class AdminDeleteUser(Form):
    username_delete = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Delete User')


class AdminWarningEmail(Form):
    username_warning = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    submit2 = SubmitField('Send Warning Email')


class DeleteAccountForm(Form):
    submit = SubmitField('Delete Account')


class AdminCustomEmailForm(Form):
    username_custom = StringField('Username:', validators=[DataRequired(), Length(1, 64)])
    custom_email_box = TextAreaField('Write the body of the email here:', validators=[DataRequired()])
    submit3 = SubmitField('Send Custom Email')
