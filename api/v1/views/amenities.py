#!/usr/bin/python3
"""
Amenity view for RESTFull Api V1
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all():
    """
    get_all method that return all the objects of class amenity
    Return:
        List with Json Object
    """
    return jsonify(
        [
            amenity.to_dict() for amenity in storage.all(Amenity).values()
        ]
    )


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET']
)
def get_by_id(amenity_id):
    """
    get_by_id method that return amenity object by id
    Arguments:
        amenity_id: Id of amenity
    Return:
        Json Object
    """
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)
    return jsonify(amenity_by_id.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_by_id(amenity_id):
    """
    delete_by_id method that delete amenity object by id
    Arguments:
        amenity_id: Id of amenity
    Return:
        empty dictionary
    """
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)
    storage.delete(amenity_by_id)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_create():
    """
    post_create method that create a new amenity object
    Return:
        Json Object with the new amenity
    """
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    elif 'name' not in new_requ:
        abort(400, 'Missing name')
    new_amenity = Amenity(**request.get_json())
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['PUT']
)
def put_update(amenity_id):
    """
    put_update method that updating a amenity by id
    Arguments:
        amenity_id: Id of amenity
    Return:
        Json Object
    """
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id:
        for attr, value in request.get_json().items():
            setattr(amenity_by_id, attr, value)
        storage.save()
        return jsonify(amenity_by_id.to_dict()), 200
    abort(404)
