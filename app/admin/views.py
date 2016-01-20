from flask import render_template, redirect, request, url_for, flash, Markup
from . import admin
from .forms import adminForm
from .webcrawler import webcrawler
from app import db
import re
import requests
from bs4 import BeautifulSoup

@admin.route('/admin', methods=['GET', 'POST'])
def admin():
    form = adminForm()
    if form.validate_on_submit():
        return webcrawler()
    return render_template('admin.html', form=form)


