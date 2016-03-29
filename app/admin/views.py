from flask import render_template, redirect, request, url_for, flash
from . import admin
from .forms import adminCustomEmailForm, adminDeleteUser, adminWarningEmail, deleteAccountForm
from wtforms import SelectField, FieldList, SubmitField
from flask.ext.wtf import Form
from .webcrawler import webcrawler
from .uniwebcrawler import uniwebcrawler
from .qualifications import setup
from ..models import Permission, Career, User, Subject, Field, ReportedComment
from ..decorators import admin_required
from ..email import send_email


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
    form1 = adminDeleteUser()
    form2 = adminWarningEmail()
    form3 = adminCustomEmailForm()
    users = User.query.all()
    username = form1.usernamedelete.data
    username2 = form2.usernamewarning.data
    username3 = form3.usernamecustom.data
    customemail = form3.customeemailbox.data
    user = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(username=username2).first()
    user3 = User.query.filter_by(username=username3).first()
    if form1.validate_on_submit():
        if user:
            flash("An email has been sent to " + username + " regarding their deleted account.")
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
            send_email(user3.email, 'Reflective Pathways Admin Message', 'auth/email/custom-email', customemail=customemail, user=user3)
            flash("A custom email you have written has been sent to " + username3 + ".")
            return redirect(url_for("admin.users"))
    return render_template('admin-users.html', users=users, form1=form1, form2=form2, form3=form3)


@admin.route('/reportedcomments', methods=['GET', 'POST'])
@admin_required
def reportedcomments():
    reported_comments = ReportedComment.query.all()
    # commentform = adminReportComment()
    # comm_id = commentform.commentid.data
    # r_comment = ReportedComment.query.filter_by(comment_id=comm_id).first()
    # if commentform.validate_on_submit():
    #     if r_comment:
    #         r_comment.remove_comment()
    #         flash('The comment with ID: ' + comm_id + ' has been successfully deleted.')
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
    form1 = deleteAccountForm()
    user = User.query.filter_by(username=username).first()
    if form1.validate_on_submit():
        send_email(user.email, 'Deletion of account', 'auth/email/delete-notice', user=user)
        User.query.filter_by(username=username).delete()
        flash("Your account has successfully been deleted.")
        return redirect(url_for('admin.index'))
    return render_template('admin-delete-user.html', form1=form1, username=username)


@admin.route('/set-course-fields', methods=['GET', 'POST'])
@admin_required
def set_subject_fields():

    all_fields_choices = sorted([(x.id, x.name) for x in Field.query.all()], key=lambda z: z[1])
    all_fields_choices.insert(0, (-1, 'None'))

    # setattr(SetField, 'fields', FieldList(SelectField('Course', choices=all_fields_choices)))
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
            flash('An error occured as the subject/fields have been changed by someone since you first loaded the page')
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


