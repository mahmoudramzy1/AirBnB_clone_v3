#!/usr/bin/python3
from flask import Blueprint
"""make blueprint of app_view"""


app_views = Blueprint('app', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
