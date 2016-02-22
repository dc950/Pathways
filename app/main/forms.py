from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DateField, FormField, SelectField
from wtforms.validators import Length


class EditProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(0, 64)])
    last_name = StringField('Last Name', validators=[Length(0, 64)])
    default_avatar = SelectField('Default avatar style.  For a custom avatar got to www.gravatar.com', choices=[
        ('mm', 'Default image'), ('identicon', 'Identicon'), ('monsterid', 'Monster'), ('wavatar', 'Wavatar'),
        ('retro', 'Retro')])
    submit = SubmitField('Submit')


class SubjectGrade(Form):
    subject_name = StringField('Subject', validators=[Length(1, 64)])
    subject_grade = StringField('Grade', validators=[Length(1, 64)])


class AddQualificationForm(Form):
    qualification_type = SelectField(u'Programming Language', coerce=int)
    """start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')"""
    """institute = StringField('Institute', validators=[Length(1, 64)])
    subject_grade_one = FormField(SubjectGrade, 'Test')"""
    """subject_grade_two = FormField(SubjectGrade)
    subject_grade_three = FormField(SubjectGrade)"""
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
