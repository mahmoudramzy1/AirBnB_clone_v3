#!/usr/bin/python3
"""API Routes for States.

This module defines the API routes for handling states in the Flask app.
It includes route handlers for retrieving all states,
retrieving a specific state by ID, creating a new state,
updating an existing state, and deleting a state.

Routes:
- GET /states: Retrieve all states.
- GET /states/<state_id>: Retrieve a specific state by ID.
- DELETE /states/<state_id>: Delete a state.
- POST /states/: Create a new state.
- PUT /states/<state_id>: Update an existing state.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """Retrieve all states.

    Returns:
        A JSON response containing a list of all states.
    """
    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Retrieve a specific state by ID.

    Args:
        state_id: The ID of the state to retrieve.

    Returns:
        A JSON response containing the details of the specified state.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Delete a state.

    Args:
        state_id: The ID of the state to delete.

    Returns:
        An empty JSON response.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states/", strict_slashes=False, methods=["POST"])
def post_state():
    """Create a new state.

    Returns:
        A JSON response containing the details of the newly created state.

    Raises:
        400: If the request data is not a valid JSON
             or if the 'name' field is missing.
    """
    state_data = request.get_json(force=True, silent=True)
    if type(state_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in state_data:
        new_state = classes["State"](**state_data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id):
    """Update an existing state.

    Args:
        state_id: The ID of the state to update.

    Returns:
        A JSON response containing the updated details of the state.

    Raises:
        404: If the state with the specified ID does not exist.
        400: If the request data is not a valid JSON.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    data_json = request.get_json(force=True, silent=True)
    if type(data_json) is not dict:
        abort(400, "Not a JSON")

    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict())
