#!/usr/bin/python3
"""
View for Reviews
"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_tasks12(place_id):
    """Show all the reviews by place"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    return jsonify([review.to_dict() for review in place_by_id.reviews])


@app_views.route('/reviews/<review_id>/', strict_slashes=False,
                 methods=['GET'])
def get_task12(review_id):
    """Return the data of a specific review"""
    review_by_id = storage.get(Review, review_id)
    if review_by_id is None:
        abort(404)
    return jsonify(review_by_id.to_dict())


@app_views.route('/reviews/<review_id>/', strict_slashes=False,
                 methods=['DELETE'])
def delete_task12(review_id):
    """Deleting a specific review by id"""
    review_by_id = storage.get(Review, review_id)
    if review_by_id is None:
        abort(404)
    else:
        storage.delete(review_by_id)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_task12(place_id):
    """Create new review"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_requ:
        abort(400, 'Missing user_id')
    user_id = request.get_json()["user_id"]
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    if 'text' not in new_requ:
        abort(400, 'Missing text')
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.user_id = user_by_id.id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_task12(review_id):
    """Updating a reviewr"""
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    review_by_id = storage.get(Review, review_id)
    if review_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(review_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_ad' and attr != 'user_id' and
                    attr != 'place_id'):
                setattr(review_by_id, attr, value)
        storage.save()
        return jsonify(review_by_id.to_dict()), 200
    abort(404)
