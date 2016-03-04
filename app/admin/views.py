from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import *
from .webcrawler import webcrawler
from .uniwebcrawler import uniwebcrawler
from .qualifications import Setup
from ..models import Permission, Career
from ..decorators import permission_required, admin_required


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


@admin.route('/users')
# @admin_required
def users():
    return render_template('admin-users.html')


@admin.route('/get-careers')
# @admin_required
def get_careers():
    webcrawler()
    flash("Careers Loaded")
    return redirect(url_for('admin.index'))


@admin.route('/insert-qualifications')
def insert_qualifications():
    Setup()


@admin.route('/load-uni-courses')
def uni_courses():
    uniwebcrawler()
    return redirect(url_for("admin.database"))
