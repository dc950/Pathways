from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FormField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import User


class EditProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(0, 64)])
    last_name = StringField('Last Name', validators=[Length(0, 64)])
    submit = SubmitField('Submit')

class SubjectGrade(Form):
	subject_name = StringField('Subject', validators=[Length(0, 32)])
	subject_grade = StringField('Grade', validators=[Length(0, 8)])

class AddQualificationForm(Form):
	qualification_type = StringField('Qualification', validators=[Length(0, 64)])
	start_date = DateField('Start Date', format='%Y-%m-%d')
	end_date = DateField('End Date', format='%Y-%m-%d')
	institute = StringField('Institute', validators=[Length(0, 64)])
	subject_grade_one = FormField(SubjectGrade, 'Test')
	subject_grade_two = FormField(SubjectGrade)
	subject_grade_three = FormField(SubjectGrade)
	submit = SubmitField('Submit')

class EditQualificationForm(Form):
	qualification_type = StringField('Qualification', validators=[Length(0, 64)])
	start_date = DateField('Start Date', format='%Y-%m-%d')
	end_date = DateField('End Date', format='%Y-%m-%d')
	institute = StringField('Institute', validators=[Length(0, 64)])
	subject_grade_one = FormField(SubjectGrade)
	submit = SubmitField('Submit')


