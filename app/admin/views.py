from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import adminForm
from .webcrawler import webcrawler
from ..models import Career
from app import db
import re
import requests
from bs4 import BeautifulSoup

@admin.route('/admin', methods=['GET', 'POST'])
def admin():
    form = adminForm()
    if form.validate_on_submit():
        webcrawler()
    careers = Career.query.all()
    return render_template('admin.html', form=form, careers=careers)


