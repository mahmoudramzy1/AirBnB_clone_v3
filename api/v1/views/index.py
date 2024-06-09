#!/usr/bin/python3
""" Index """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """retrun status json"""
    return jsonify({"status": "OK"})
