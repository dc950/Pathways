from flask import render_template, redirect, request, url_for, flash
from . import admin
from .forms import AdminCustomEmailForm, AdminDeleteUser, AdminWarningEmail, DeleteAccountForm
from wtforms import SelectField, FieldList, SubmitField
from flask.ext.wtf import Form
from .webcrawler import webcrawler
from .uniwebcrawler import uniwebcrawler
from .qualifications import setup
from ..models import Permission, Career, User, Subject, Field, ReportedComment, UserQualification
from ..decorators import admin_required
from ..email import send_email
from app import db


@admin.route('/')
@admin.route('/index/')
@admin_required
def index():
    return render_template('admin-index.html')


@admin.route('/database', methods=['GET', 'POST'])
@admin_required
def database():
    careers = Career.query.all()
    return render_template('admin-database.html', careers=careers)


@admin.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
    form1 = AdminDeleteUser()
    form2 = AdminWarningEmail()
    form3 = AdminCustomEmailForm()
    username = form1.username_delete.data
    username2 = form2.username_warning.data
    username3 = form3.username_custom.data
    custom_email = form3.custom_email_box.data
    user = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(username=username2).first()
    user3 = User.query.filter_by(username=username3).first()
    number_of_users = 0
    all_users = User.query.all()
    for x in all_users:
        if x.is_active:
            number_of_users += 1
    if form1.validate_on_submit():
        if user:
            return redirect(url_for('admin.delete_this_user', username=username))
        else:
            flash('Username doesnt exist')
    if form2.validate_on_submit():
        if user2:
            send_email(user2.email, 'Inappropriate profile avatar', 'auth/email/avatar-warning', user=username2)
            # user2.def_avatar = 'mm'
            user2.remove_permission(Permission.HAVE_AVATAR)
            flash("A warning email has been sent to " + username2 + "'s email address.")
            return redirect(url_for("admin.users"))
        else:
            flash('Username doesnt exist')
    if form3.validate_on_submit():
        if user3:
            send_email(user3.email, 'Reflective Pathways Admin Message', 'auth/email/custom-email', customemail=custom_email, user=user3)
            flash("A custom email you have written has been sent to " + username3 + ".")
            return redirect(url_for("admin.users"))
    return render_template('admin-users.html', users=all_users, form1=form1, form2=form2, form3=form3, numberofusers=number_of_users)


@admin.route('/reportedcomments', methods=['GET', 'POST'])
@admin_required
def reportedcomments():
    reported_comments = ReportedComment.query.all()
    return render_template('admin-reportedcomments.html', reported_comments=reported_comments)


@admin.route('/deletecomment/<commentid>', methods=['GET', 'POST'])
@admin_required
def deletecomment(commentid):
    r_comment_obj = ReportedComment.query.filter_by(comment_id=commentid).first()
    if r_comment_obj is None:
        flash('This comment doesnt exist')
        return redirect(url_for('admin.reportedcomments'))
    r_comment_obj.remove_comment()
    flash('This comment has been successfully deleted.')
    return redirect(url_for('admin.reportedcomments'))


@admin.route('/keepcomment/<commentid>', methods=['GET', 'POST'])
@admin_required
def keepcomment(commentid):
    r_comment_obj = ReportedComment.query.filter_by(comment_id=commentid).first()
    if r_comment_obj is None:
        flash('This comment doesnt exist')
        return redirect(url_for('admin.reportedcomments'))
    r_comment_obj.keep_comment()
    flash('This comment has been not been deleted.')
    return redirect(url_for('admin.reportedcomments'))


@admin.route('/get-careers')
@admin_required
def get_careers():
    webcrawler()
    flash("Careers Loaded")
    return redirect(url_for('admin.index'))


@admin.route('/insert-qualifications')
@admin_required
def insert_qualifications():
    setup()


@admin.route('/load-uni-courses')
@admin_required
def uni_courses():
    uniwebcrawler()
    return redirect(url_for("admin.database"))


@admin.route('/delete-user/<username>', methods=['GET', 'POST'])
@admin_required
def delete_this_user(username):
    form1 = DeleteAccountForm()
    user = User.query.filter_by(username=username).first()
    if form1.validate_on_submit():
        send_email(user.email, 'Deletion of account', 'auth/email/delete-notice', user=user)
        # Find and delete UserQualifications
        uqs = UserQualification.query.filter_by(user_id=user.id).all()
        for uq in uqs:
            db.session.delete(uq)

        # Find and delete skills
        for s in user.skills:
            user.skills.remove(s)

        # Remove connections
        for i in user.connection_requests:
            user.connection_requests.remove(i)

        for i in user.connection_invitations:
            user.connection_invitations.remove(i)

        # Remove future quals
        for q in user.future_quals:
            user.future_quals.remove(q)

        # Remove future careers
        for c in user.future_careers:
            user.future_careers.remove(c)

        user.first_name = ''
        user.last_name = ''
        user.email = str(user.id)
        user.username = str(user.id)
        user.avatar_hash = ''

        user.is_active = False
        flash("The account has successfully been deleted.")
        flash("An email has been sent to " + username + " regarding their deleted account.")
        return redirect(url_for('admin.index'))
    return render_template('admin-delete-user.html', form1=form1, username=username)


@admin.route('/set-course-fields', methods=['GET', 'POST'])
@admin_required
def set_subject_fields():

    all_fields_choices = sorted([(x.id, x.name) for x in Field.query.all()], key=lambda z: z[1])
    all_fields_choices.insert(0, (-1, 'None'))

    class SetField(Form):
        fields = FieldList(SelectField('course', choices=all_fields_choices))
        submit = SubmitField('Submit')

    form = SetField(request.form)
    subjects = Subject.query.filter_by(field=None).all()
    f_data = form.fields.data

    # Doing this instead of validate_on_submit because it's never True for some reason I can't figure out
    # This is probably less secure but it is in the admin section so it shouldn't be too big a risk...
    if len(f_data) > 0:
        if len(f_data) != len(subjects):
            flash('An error occurred as the subject/fields have been changed by someone since you first loaded the page')
        for s, f in zip(subjects, form.fields.data):
            if f != '-1':
                field = Field.query.filter_by(id=f).first()
                s.field = field
        return redirect(url_for('admin.set_subject_fields'))

    form_data = []
    for s in subjects:
        e = form.fields.append_entry(s.name)
        form_data.append((s.name, e))

    return render_template('admin-fields.html', form=form, form_data=form_data)


