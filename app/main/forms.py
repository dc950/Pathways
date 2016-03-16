from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DateField, FormField, SelectField, TextAreaField, HiddenField
from wtforms.validators import Length
from ..models import User, UserQualification, Qualification, QualificationType, Career
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class SkillsForm(Form):
    skills = TextAreaField();
    skillsHidden = HiddenField("Skills")


class EditProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(0, 64)])
    last_name = StringField('Last Name', validators=[Length(0, 64)])
    email = StringField('If you would like to change your email, please edit the text box below.', validators=[Length(0, 64)])
    default_avatar = SelectField('Default avatar style.  For a custom avatar got to www.gravatar.com', choices=[
        ('mm', 'Default image'), ('identicon', 'Identicon'), ('monsterid', 'Monster'), ('wavatar', 'Wavatar'),
        ('retro', 'Retro')])
    s = FormField(SkillsForm)
    submit = SubmitField('Submit')


class SubjectGrade(Form):
    subject_name = StringField('Subject', validators=[Length(1, 64)])
    subject_grade = StringField('Grade', validators=[Length(1, 64)])


class AddQualificationForm(Form):
    qualification_type = SelectField(u'Qualification', coerce=int)
    subjects = SelectField(u'Subject 1', coerce=int)
    grade = StringField('Grade', validators=[Length(1, 64)])
    submit = SubmitField('Submit')


class EditQualificationForm(Form):
    qualification_type = StringField('Qualification', validators=[Length(0, 64)])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    institute = StringField('Institute', validators=[Length(0, 64)])
    subject_grade_one = FormField(SubjectGrade)
    submit = SubmitField('Submit')


class SearchForm(Form):
    term = StringField('Search', validators=[Length(1, 64)])
    submit = SubmitField('Search')


class CommentForm(Form):
    body = StringField('Comment', validators=[Length(1, 256)])
    submit = SubmitField("Submit")
