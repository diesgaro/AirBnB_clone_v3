#!/usr/bin/python3
"""
View to handle all default RestFull API actions
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_task7():
    """Entry method, response in json format"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_tasks7(state_id):
    """Return the data of a specific state"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    return jsonify(state_by_id.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_task7(state_id):
    """Deleting a specific state by id"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    storage.delete(state_by_id)
    storage.save()
    return jsonify({})


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_task7():
    """Create new state"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    elif 'name' not in new_requ:
        abort(400, 'Missing name')
    new_state = State(**request.get_json())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_task7(state_id):
    """Updating a state"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        for attr, value in request.get_json().items():
            setattr(state_by_id, attr, value)
        storage.save()
        return jsonify(state_by_id.to_dict()), 200
    abort(404)
