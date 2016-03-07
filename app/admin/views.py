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
# @admin_required
def index():
    return render_template('admin-index.html')


@admin.route('/database', methods=['GET', 'POST'])
# @admin_required
def database():
    careers = Career.query.all()
    return render_template('admin-database.html', careers=careers)


@admin.route('/users', methods=['GET', 'POST'])
# @admin_required
def users():
    form1 = adminDeleteUser()
    form2 = adminWarningEmail()
    users = User.query.all()
    username = form1.usernamedelete.data
    username2 = form2.usernamewarning.data
    user = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(username=username2).first()
    if form1.validate_on_submit():
        if user:
            flash("An email has been sent to your email address with more instructions on how to delete your account.")
            return redirect(url_for('admin.delete_this_user', username=username))
        else:
            flash('Username doesnt exist')
    if form2.validate_on_submit():
        if user2:
            send_email(user2.email, 'Inappropriate profile avatar', 'auth/email/avatar-warning', user=username2)
            user2.def_avatar = 'mm'
            flash("A warning email has been sent to " + username2 + "'s email address.")
            return redirect(url_for("admin.users"))
        else:
            flash('Username doesnt exist')
    return render_template('admin-users.html', users=users, form1=form1, form2=form2)




@admin.route('/get-careers')
# @admin_required
def get_careers():
    webcrawler()
    flash("Careers Loaded")
    return redirect(url_for('admin.index'))


#@admin.route('/insert-qualifications')
#def insert_qualifications():
#    qualifications()


@admin.route('/load-uni-courses')
def uni_courses():
    uniwebcrawler()
    return redirect(url_for("admin.database"))

@admin.route('/delete-user/<username>', methods=['GET', 'POST'])
def delete_this_user(username):
    form1 = deleteAccountForm()
    user = User.query.filter_by(username=username).first()
    if form1.validate_on_submit():
        send_email(user.email, 'Deletion of account', 'auth/email/delete-notice', user=user)
        User.query.filter_by(username=username).delete()
        flash("Your account has successfully been deleted.")
        return redirect(url_for('admin.index'))
    return render_template('admin-delete-user.html', form1=form1, username = username)
