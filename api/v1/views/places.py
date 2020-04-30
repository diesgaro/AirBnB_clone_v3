#!/usr/bin/python3
"""
Places view for RESTFull Api V1
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET']
)
def get_all_places_by_city(city_id):
    """
    get_all_places_by_city method that retrieves all the objects of places
    class by city
    Arguments:
        city_id = Id of city
    Return:
        Json Object
    """
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    return jsonify(
        [
            place.to_dict() for place in city_by_id.places
        ]
    )


@app_views.route(
    '/places/<place_id>/',
    strict_slashes=False,
    methods=['GET'])
def get_place_by_id(place_id):
    """
    get_place_by_id method that return place object by id
    Arguments:
        place_id: Id of place
    Return:
        Json Object
    """
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    return jsonify(place_by_id.to_dict())


@app_views.route(
    '/places/<place_id>/',
    strict_slashes=False,
    methods=['DELETE'])
def delete_place_by_id(place_id):
    """
    delete_place_by_id method that delete place object by id
    Arguments:
        place_id: Id of place
    Return:
        empty dictionary
    """
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    else:
        storage.delete(place_by_id)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places",
    strict_slashes=False,
    methods=['POST']
)
def post_create_place(city_id):
    """
    post_create_place method that create a new place object
    Arguments:
        city_id: Id of city to the new place
    Return:
        Json Object with the new place
    """
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    if 'name' not in new_requ:
        abort(400, 'Missing name')
    if 'user_id' not in new_requ:
        abort(400, 'Missing user_id')

    user_id = new_requ['user_id']
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.user_id = user.id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['PUT'])
def put_update_place(place_id):
    """
    put_update_place method that updating a place by id
    Arguments:
        place_id: Id of place
    Return:
        Json Object
    """
    new_requ = request.get_json()
    if not new_requ:
        abort(400, 'Not a JSON')
    place_by_id = storage.get(Place, place_id)
    if place_by_id:
        for attr, value in request.get_json().items():
            setattr(place_by_id, attr, value)
        storage.save()
        return jsonify(place_by_id.to_dict()), 200
    abort(404)
