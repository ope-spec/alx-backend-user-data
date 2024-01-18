#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    Get a list of all User objects in JSON representation.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    Get JSON representation of a single User object.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    if request.current_user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    Delete a User object and return an empty JSON if successful.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    Create a new User object and return its JSON representation
    """
    user_data = None
    error_msg = None
    try:
        user_data = request.get_json()
    except Exception as e:
        user_data = None
    if user_data is None:
        error_msg = "Wrong format"
    if error_msg is None and user_data.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and user_data.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = user_data.get("email")
            user.password = user_data.get("password")
            user.first_name = user_data.get("first_name")
            user.last_name = user_data.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    Update a User object and return its JSON representation.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user_data = None
    try:
        user_data = request.get_json()
    except Exception as e:
        user_data = None
    if user_data is None:
        return jsonify({'error': "Wrong format"}), 400
    if user_data.get('first_name') is not None:
        user.first_name = user_data.get('first_name')
    if user_data.get('last_name') is not None:
        user.last_name = user_data.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
