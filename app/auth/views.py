from flask import render_template, redirect, request, url_for, flash, Markup, current_app, get_flashed_messages
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, UserQualification, user_skills, connections, future_quals, future_careers
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ForgottenPasswordForm, DeleteAccountForm
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data) and user.is_active:
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
        db.session.commit()
        user.send_confirmation_email()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/forgotten-password', methods=['GET', 'POST'])
def forgotten_password():
    form = ForgottenPasswordForm()
    if form.validate_on_submit():
        return send_new_password_email(email=form.email.data)
    return render_template('forgotten-password.html', form=form)


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


@auth.route('/send-new-password-email')
def send_new_password_email(email=None):
    if email is not None:
        user = User.query.filter_by(email=email).first()
        if user:
            user.send_new_password_email()
            return redirect(url_for('auth.login'))
        else:
            flash('No user with that associated account was found.  Please register to create an account')
            return redirect(url_for('auth.register'))
    else:
        # Request was made from a user.
        if current_user.confirmed is True:
            current_user.send_new_password_email()
        else:
            flash("You must authenticate your account before you can do this action. Please see your email to authenticate your account.")
        return redirect(url_for('main.edit'))

@auth.route('/change-password/<token>', methods=['GET', 'POST'])
def change_password(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        flash("The url you used is either invalid or has expired.")
        return redirect(url_for('main.index'))
    # Find the user from the token
    uid = data.get('new_password')
    user = User.query.filter_by(id=uid).first()
    # If the user is not found, there's a problem...
    if not user:
        flash("The url you used is either invalid or has expired.")
        return redirect(url_for('main.index'))
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        if current_user.is_authenticated:
            logout_user()
        flash("Your password has been changed successfully.  Please login with your new password to continue")
        return redirect(url_for('auth.login'))
    return render_template('new_password.html', form=form)


@auth.route('/delete-account/<token>', methods=['GET', 'POST'])
@login_required
def delete_account(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        flash("The url you used is either invalid or has expired.")
        return redirect(url_for('main.index'))
    # Find the user from the token
    uid = data.get('delete_account')
    user = User.query.filter_by(id=uid).first()
    # If the user is not found, there's a problem...
    if not user:
        flash("The url you used is either invalid or has expired.")
        return redirect(url_for('main.index'))
    form = DeleteAccountForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:

            # Find and delete UserQualificaions
            uqs = UserQualification.query.filter_by(user_id=current_user.id).all()
            for uq in uqs:
                db.session.delete(uq)

            # Find and delete skills
            for s in current_user.skills:
                current_user.skills.remove(s)

            # Remove connections
            for i in current_user.connection_requests:
                current_user.connection_requests.remove(i)

            for i in current_user.connection_invitations:
                current_user.connection_invitations.remove(i)

            # Remove future quals
            for q in current_user.future_quals:
                current_user.future_quals.remove(q)

            # Remove future careers
            for c in current_user.future_careers:
                current_user.future_careers.remove(c)

            current_user.first_name = ''
            current_user.last_name = ''
            current_user.email = str(current_user.id)
            current_user.username = str(current_user.id)
            current_user.avatar_hash = ''


            current_user.is_active = False
            logout_user()
            # User.query.filter_by(id=uid).delete()
            flash("Your account has successfully been deleted.")
            return redirect(url_for('main.index'))
    return render_template('delete_account.html', form=form)

@auth.route('/send-new-delete_acc-email')
def send_new_delete_acc_email(email=None):
    if email is not None:
        user = User.query.filter_by(email=email).first()
        if user:
            user.send_new_delete_acc_email()
            return redirect(url_for('auth.login'))
        else:
            flash('No user with that associated account was found.  Please register to create an account')
            return redirect(url_for('auth.register'))
    else:
        # Request was made from a user.
        if current_user.confirmed is True:
            current_user.send_new_delete_acc_email()
        else:
            flash("You must authenticate your account before you can do this action. Please see your email to authenticate your account.")
        return redirect(url_for('main.edit'))

# @auth.before_app_request
# def before_request():
#     if request.endpoint:
#         if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
#             message = Markup("Note: Your account has not been authenticated yet. <a href='"+url_for('auth.send_token')+"'> Click here </a> to resend the email.")
#             # for m in get_flashed_messages():
#             #     if m == message:
#             #         return
#             flash(message)
