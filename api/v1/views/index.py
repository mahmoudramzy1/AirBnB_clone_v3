#!/usr/bin/python3
""" Index """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """retrun status json"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """return stats"""
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count = {}
    for key, value in classes.items():
        count[key] = storage.count(value)
    return jsonify(count)
