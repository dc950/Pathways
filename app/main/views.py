from flask import render_template, session, flash, redirect, url_for, send_from_directory
from flask.ext.login import current_user, login_required
from . import main
from .. import db
from ..models import User
from .forms import EditProfileForm


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html",
                           title="Home")


@main.route('/user/<username>')
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        flash('User %s not found.' % username)
        return redirect(url_for('main.index'))
    name = user_obj.first_name + " " + user_obj.last_name
    return render_template("user.html",
                           user=user_obj,
                           title=name + " | pathways")


@login_required
@main.route('/user/edit-profile', methods=['GET', 'POST'])

def edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user', user_id=current_user.id))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    return render_template('edit-profile.html', form=form)

@main.route('/user/pathway/edit-qualification')
def editQualification():
    return render_template("edit-qualificaiton.html",
                           title="Edit Qualification")


@login_required
@main.route('/connections')
def connections():
    users = User.query.all()
    return render_template('connections.html',
                           users=users)


@main.route('/about')
def about():
    return render_template("about.html",
                           title="Test")


@main.route('/user/pathway')
def pathway():
    return render_template("pathway.html",
                           title="Test")


@main.route('/add_connection/<username>')
@login_required
def add_connection(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj is None:
        flash('User does not exist')
        return redirect(url_for('.index'))
    if current_user.made_request(user_obj):
        flash('You have already made a request to this person')
        return redirect(url_for('.user', username=user_obj.username))
    user_obj.send_request(current_user)
    if user_obj in current_user.connections:
        flash('You are now connected with %s.' % (user_obj.first_name + " " + user_obj.last_name))
    else:
        flash('Request sent to %s.' % (user_obj.first_name + " " + user_obj.last_name))
    return redirect(url_for('.user', username=username))


@main.route('/test')
def test():
    return render_template("test.html",
                           title="Test")


@main.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js/pathways.js')


@main.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


'''
/
/user/
/user/edit-profile
/user/pathways
/user/pathways/edit-qualification 
'''
