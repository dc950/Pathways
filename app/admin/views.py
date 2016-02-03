from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import adminForm
from .webcrawler import webcrawler
from app import db
import re
import requests
from bs4 import BeautifulSoup

@admin.route('/admin/index')
@admin.route('/admin/')
def index():
    return render_template('admin-index.html')

@admin.route('/admin/database', methods=['GET', 'POST'])
def database():
    form = adminForm()
    if form.validate_on_submit():
        return webcrawler()
    return render_template('admin-database.html', form=form)

@admin.route('/admin/users')
def users():
    return render_template('admin-users.html')


