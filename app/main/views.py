from flask import render_template, session, flash, redirect, url_for
from flask.ext.login import current_user
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


@main.route('/edit', methods=['GET', 'POST'])
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
    return render_template('edit.html', form=form)


@main.route('/about')
def about():
    return render_template("about.html",
                           title="Test")


@main.route('/pathway')
def pathway():
    return render_template("pathway.html",
                           title="Test")


@main.route('/test')
def test():
    return render_template("test.html",
                           title="Test")


@main.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@main.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)
