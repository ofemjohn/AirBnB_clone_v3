#!/usr/bin/python3
"""
Flask route that returns json status response for all User Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_users():
    """
    list or add users to stroage
    """
    if request.method == 'GET':
        users = storage.all(User)
        return jsonify(
            [user.to_dict() for user in users.values()]
        )
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("email") is None:
            abort(400, "Missing email")
        if data.get("password") is None:
            abort(400, "Missing password")
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_user(user_id):
    """
    get, delete or update particular user and user is
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            user.to_dict()
        )
    if request.method == 'DELETE':
        user.delete()
        del user
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(user, key, val)
        user.save()
        return jsonify(user.to_dict()), 200
