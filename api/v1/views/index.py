#!/usr/bin/python3
"""Index file for API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats',  methods=['GET'], strict_slashes=False)
def stats():
    """Returns status of all classes"""
    all_type = {"amenities": "Amenity", "cities": "City", "places": "Place",
                "reviews": "Review", "states": "State", "users": "User"}
    stats_object_by_type = {}
    for element in all_type:
        stats_object_by_type[element] = storage.count(all_type[element])
    stats_object_by_type = jsonify(stats_object_by_type)
    stats_object_by_type.status = 200

    return stats_object_by_type
