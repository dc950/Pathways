from flask import render_template, flash, redirect, url_for
from app import app, models


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="Home")


@app.route('/user/<user_id>')
def user(user_id):
    user_obj = models.User.query.filter_by(id=user_id).first()
    if user_obj is None:
        flash('User %s not found.' % user_id)
        return redirect(url_for('index'))
    name = user_obj.first_name + " " + user_obj.last_name
    return render_template("user.html",
                           user=user_obj,
                           title=name + "| pathways")
