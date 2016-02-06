from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import adminForm
from .webcrawler import webcrawler
from ..models import Permission
from ..decorators import permission_required, admin_required


@admin.route('/')
@admin.route('/index/')
@admin_required
def index():
    return render_template('admin-index.html')


@admin.route('/database', methods=['GET', 'POST'])
@admin_required
def database():
    form = adminForm()
    if form.validate_on_submit():
        webcrawler()
    return render_template('admin-database.html', form=form)


@admin.route('/users')
@admin_required
def users():
    return render_template('admin-users.html')


