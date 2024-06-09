#!/usr/bin/python3
from flask import Blueprint
from api.v1.views.index import *
"""make blueprint of app_view"""

app_views = Blueprint('app', __name__, url_prefix='/api/v1')
