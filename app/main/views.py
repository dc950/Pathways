from flask import render_template, session, flash, redirect, url_for
from . import main
from .. import db
from ..models import User


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html",
                           title="Home")


@main.route('/user/<user_id>')
def user(user_id):
    user_obj = User.query.filter_by(id=user_id).first()
    if user_obj is None:
        flash('User %s not found.' % user_id)
        return redirect(url_for('main.index'))
    name = user_obj.first_name + " " + user_obj.last_name
    return render_template("user.html",
                           user=user_obj,
                           title=name + " | pathways")

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
