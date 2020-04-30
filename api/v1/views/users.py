#!/usr/bin/python3
"""
View for Users
"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def users():
    """Show all the users"""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>/', strict_slashes=False,
                 methods=['GET'])
def get_task10(user_id):
    """Return the data of a specific user"""
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    return jsonify(user_by_id.to_dict())


@app_views.route('/users/<user_id>/', strict_slashes=False,
                 methods=['DELETE'])
def delete_task10(user_id):
    """Deleting a specific user by id"""
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    else:
        storage.delete(user_by_id)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", strict_slashes=False,
                 methods=['POST'])
def post_task10():
    """Create new user"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    if 'email' not in new_requ:
        abort(400, 'Missing email')
    if 'password' not in new_requ:
        abort(400, 'Missing password')
    new_user = User(**request.get_json())
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_task10(user_id):
    """Updating an user"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    user_by_id = storage.get(User, user_id)
    if user_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(user_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_ad') and attr != 'email':
                setattr(user_by_id, attr, value)
        storage.save()
        return jsonify(user_by_id.to_dict()), 200
    abort(404)
