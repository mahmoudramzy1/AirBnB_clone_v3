#!/usr/bin/python3
"""A  view for State objects that handles all default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/api/v1/states', methods=['GET'])
def get_states():
    """Get a list of all state objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get a state object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state object"""
    if not request.json:
        return abort(400, 'Not a JSON')
    if 'name' not in request.json:
        return abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
