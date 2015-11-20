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
