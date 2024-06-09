from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify
"""first status"""


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """return status"""
    return jsonify({ "status": "OK" })
