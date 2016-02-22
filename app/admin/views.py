from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import *
from .webcrawler import webcrawler
from .qualifications import *
from ..models import Permission, Career
from ..decorators import permission_required, admin_required


@admin.route('/')
@admin.route('/index/')
def index():
    return render_template('admin-index.html')


@admin.route('/database', methods=['GET', 'POST'])
def database():
    form1 = qualTypesForm()
    form2 = qualTypesForm()
    careers = Career.query.all()
    if form1.validate_on_submit():
        qualifications()
        subjects()
    return render_template('admin-database.html', form2=form2, form1=form1)


@admin.route('/users')
def users():
    return render_template('admin-users.html')


