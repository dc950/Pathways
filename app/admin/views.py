from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import *
from .webcrawler import webcrawler
from .uniwebcrawler import uniwebcrawler
from .qualifications import *
from ..models import Permission, Career, User
from ..decorators import permission_required, admin_required
from flask import render_template, redirect, request, url_for, flash, Markup, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
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


@admin.route('/get-careers')
@admin_required
def get_careers():
    webcrawler()
    flash("Careers Loaded")
    return redirect(url_for('admin.index'))


@admin.route('/insert-qualifications')
@admin_required
def insert_qualifications():
    Setup(False)


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
    return render_template('admin-delete-user.html', form1=form1, username = username)
