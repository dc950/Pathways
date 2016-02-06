from flask import Blueprint
from ..models import Permission

admin = Blueprint('admin', __name__)


@admin.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from . import views
