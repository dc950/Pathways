from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import Length, DataRequired,  ValidationError
from ..models import QualificationType
import re


class SkillsForm(Form):
    skills = TextAreaField()
    skillsHidden = HiddenField("Skills")


class EditProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(1, 64), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(1, 64), DataRequired()])
    default_avatar = SelectField('Default avatar style.  For a custom avatar got to www.gravatar.com', choices=[
        ('mm', 'Default image'), ('identicon', 'Identicon'), ('monsterid', 'Monster'), ('wavatar', 'Wavatar'),
        ('retro', 'Retro')])
    submit = SubmitField('Submit')


class SubjectGrade(Form):
    subject_name = StringField('Subject', validators=[Length(1, 64)])
    subject_grade = StringField('Grade', validators=[Length(1, 64)])


class GradeCheck(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            reg_no = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)

        reg = QualificationType.query.filter_by(id=reg_no.data).first().allowed_grades

        print('field.data: '+str(field.data)+", reg: "+ reg)
        print(re.match(reg, field.data))
        if re.match(reg, field.data) is None:
            message = self.message
            if message is None:
                message = field.gettext('The grade %s is not allowed' % field.data)
            raise ValidationError(message)


class AddQualificationForm(Form):
    qualification_type = SelectField(u'Qualification', coerce=int)
    subjects = SelectField(u'Subject 1', coerce=int)
    grade = StringField('Grade', validators=[Length(1, 64), GradeCheck('qualification_type')])
    submit = SubmitField('Submit')


class EditQualificationForm(Form):
    qualification_type = SelectField(u'Qualification', coerce=int)
    subjects = SelectField(u'Subject 1', coerce=int)
    grade = StringField('Grade', validators=[Length(1, 64), GradeCheck('qualification_type')])
    submit = SubmitField('Submit')

    def get_allowed_grades(self):
        return QualificationType.query.filter_by(name=self.qualification_type.data).first().allowed_grades


class SearchForm(Form):
    term = StringField('Search', validators=[Length(1, 64)])
    submit = SubmitField('Search')


class CommentForm(Form):
    body = StringField('Comment', validators=[Length(1, 256)])
    submit = SubmitField("Submit")
