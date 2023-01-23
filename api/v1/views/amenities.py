#!/usr/bin/python3
"""
Flask route that returns json status response for all Amenities Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_amenities():
    """
    list or add amenities to stroage
    """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        return jsonify(
            [amenity.to_dict() for amenity in amenities.values()]
        )
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("name") is None:
            abort(400, "Missing name")
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_amenity(amenity_id):
    """
    get, delete or update particular amentiy given amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            amenity.to_dict()
        )
    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(amenity, key, val)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
