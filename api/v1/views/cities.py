#!/usr/bin/python3
"""
Flask route that returns json status response on City Objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_cities(state_id):
    """
    Get or add cities given a state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        cities = storage.all(City)
        return jsonify([city.to_dict() for city in cities.values()
                        if city.to_dict().get("state_id") == state_id])
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("name") is None:
            abort(400, "Missing name")
        data["state_id"] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_city(city_id):
    """
    Get, delete or update particular city given city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            city.to_dict()
        )
    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict()), 200
