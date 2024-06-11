#!/usr/bin/python3
"""create cities"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """retrieves the lisr of cities in state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """retrieve city"""
    city = storage.get(city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """delete city"""
    city = storage.get(city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """create city"""
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.get_json():
        abort(404, 'Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        return abort(404, 'Missing name')

    data['state_id'] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def edit_city(city_id):
    """create city"""
    if request.content_type != 'application/json':
        abort(404, 'Not a JSON')

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.get_json():
        abort(404, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(city, k, v)
    city.save()

    return jsonify(city.to_dict()), 200
