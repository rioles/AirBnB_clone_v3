#!/usr/bin/python3
"""Creates view for Place objects to handle default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves a list of all Place objects"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
