#!/usr/bin/python3
"""A view for User objects that handles all default RESTFul API actions"""
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/places/<place_id>/amenities', 
                 strict_slashes=False, methods=["GET"])
                """
                retrive the list of amenities from place
                """
                place = storage.get(Place, place_id)
                if not place:
                    abort(404)
                
                amenities = [amenity.to_dict() for amenity in place.amenities]
                return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
                """
                delete specified amenity
                """
                place = storage.get(Place, place_id)
                if not place:
                    abort(404)
                
                amenity = storage.get(amenity, amenity_id)
                if not amenity :
                    abort(404)

                if amenity not in place.amenities:
                    abort(404)
                
                storage.delete(amenity)
                storage.save()
                return jsonify({})

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])

                place = storage.get(Place, place_id)
                if not place:
                    abort(404)
                
                amenity = storage.get(amenity, amenity_id)
                if not amenity :
                    abort(404)
                
                if amenity in place.amenities:
                    return jsonify(amenity.to_dict())
                return jsonify(amenity.to_dict()), 201