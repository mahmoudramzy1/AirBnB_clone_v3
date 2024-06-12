#!/usr/bin/python3
"""API Routes for Amenities.

This module defines the API routes for handling amenities in the Flask app.
It includes route handlers for retrieving all amenities for a place,
deleting an amenity from a place, and adding an amenity to a place.

Routes:
- GET /places/<place_id>/amenities: Retrieve all amenities for a place.
- DELETE /places/<place_id>/amenities/<amenity_id>: Delete an amenity
                                                    from a place.
- POST /places/<place_id>/amenities/<amenity_id>: Add an amenity to a place.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False, methods=["GET"])
def get_amenities_place(place_id):
    """Get all amenities for a place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        A JSON response containing a list of all amenities for the place.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    amenities_list = []
    for amenity in place.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenity_place(place_id, amenity_id):
    """Delete an amenity from a place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity.

    Returns:
        An empty JSON response.

    Raises:
        404: If the place or amenity with the specified IDs do not exist,
             or if the amenity is not associated with the place.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def post_amenity_place(place_id, amenity_id):
    """Add an amenity to a place.

    Args:
        place_id (str): The ID of the place.
        amenity_id (str): The ID of the amenity.

    Returns:
        A JSON response containing the details of the added amenity.

    Raises:
        404: If the place or amenity with the specified IDs do not exist.
        201: If the amenity is successfully added to the place.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    amenity = storage.get(classes["Amenity"], amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    return jsonify(amenity.to_dict()), 201
