from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import *
from .webcrawler import webcrawler
from .qualifications import *
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
    form1 = qualTypesForm()
    form2 = qualTypesForm()
    careers = Career.query.all()
    if form1.validate_on_submit():
        qualifications()
        subjects()
    careers = Career.query.all()
    return render_template('admin-database.html', form2=form2, form1=form1, careers=careers)


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

