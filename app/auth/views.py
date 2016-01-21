from flask import render_template, redirect, request, url_for, flash, Markup
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/send_token')
def send_token():
    current_user.send_confirmation_email()
    return redirect(request.args.get('next') or url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data)
        user.generate_username()
        db.session.add(user)
        user.send_confirmation_email()
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account')
    else:
        flash('The confirmation link is invalid or had expired')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        message = Markup("'Note: Your account has not been authenticated yet. <a href='"+url_for('auth.send_token')+"'> Click here </a> to resend the email.'")
        flash(message)
