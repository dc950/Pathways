from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html",
                           title="Home")
@app.route('/about')
def about():
    return render_template("about.html",
                           title="Test")

@app.route('/pathway')
def pathway():
    return render_template("pathway.html",
                           title="Test")

@app.route('/test')
def test():
    return render_template("test.html",
                           title="Test")
