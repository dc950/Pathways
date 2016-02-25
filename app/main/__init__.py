from flask import Blueprint
from ..models import Permission
from .forms import SearchForm

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.app_context_processor
def inject_search():
    form = SearchForm()
    return dict(search_form=form)


from . import views, errors
