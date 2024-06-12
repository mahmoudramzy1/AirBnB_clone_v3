#!/usr/bin/python3
"""API Routes for Places.

This module defines the API routes for handling places in the Flask app.
It includes route handlers for retrieving all places in a city,
retrieving a specific place by ID, creating a new place,
updating an existing place, and deleting a place.

Routes:
- GET /cities/<city_id>/places: Retrieve all places in a city.
- GET /places/<place_id>: Retrieve a specific place by ID.
- DELETE /places/<place_id>: Delete a place.
- POST /cities/<city_id>/places: Create a new place in a city.
- POST /places_search: Search for places based on
                       states, cities, and amenities.
- PUT /places/<place_id>: Update an existing place.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
def get_places(city_id):
    """Retrieve all places in a city.

    Args:
        city_id: The ID of the city.

    Returns:
        A JSON response containing a list of all places in the city.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """Retrieve a specific place by ID.

    Args:
        place_id: The ID of the place.

    Returns:
        A JSON response containing the details of the place.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """Delete a place.

    Args:
        place_id: The ID of the place.

    Returns:
        An empty JSON response.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def post_place(city_id):
    """Create a new place in a city.

    Args:
        city_id: The ID of the city.

    Returns:
        A JSON response containing the details of the newly created place.

    Raises:
        400: If the request data is not in JSON format
             or is missing required fields.
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    place_data = request.get_json(force=True, silent=True)
    if type(place_data) is not dict:
        abort(400, "Not a JSON")

    if "user_id" not in place_data:
        abort(400, "Missing user_id")

    user_obj = storage.get(classes["User"], place_data["user_id"])
    if user_obj is None:
        abort(404)

    if "name" not in place_data:
        abort(400, "Missing name")
    else:
        new_place = classes["Place"](city_id=city_id, **place_data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", strict_slashes=False, methods=["POST"])
def post_place_search():
    """Search for places based on states, cities, and amenities.

    Returns:
        A JSON response containing the list of
        places that match the search criteria.

    Raises:
        400: If the request data is not in JSON format.
    """
    if request.get_json() is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = request.get_json().get("states", [])
    cities = request.get_json().get("cities", [])
    amenities = request.get_json().get("amenities", [])

    amenities_list = []
    for amenity_id in amenities:
        amenity = storage.get("Amenity", amenity_id)
        if amenity:
            amenities_list.append(amenity)

    if states == cities == []:
        places = storage.all("Place").values()
    else:
        places = []
        for state_id in states:
            state = storage.get("State", state_id)
            for city in state.cities:
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = storage.get("City", city_id)
            for place in city.places:
                places.append(place)

    places_list = []
    for place in places:
        places_list.append(place.to_dict())
        for amenity in amenities_list:
            if amenity not in place.amenities:
                places_list.pop()
                break
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def put_place(place_id):
    """Update an existing place.

    Args:
        place_id: The ID of the place.

    Returns:
        A JSON response containing the updated details of the place.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    place_data = request.get_json(force=True, silent=True)
    if type(place_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in place_data.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())
