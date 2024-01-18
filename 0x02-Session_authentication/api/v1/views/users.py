#!/usr/bin/env python3
"""Module for Users Views"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """
    Get a list of all User objects in JSON representation.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_one_user(user_id: str = None) -> str:
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
    Create a new User object and return its JSON representation.
    """
    request_json = None
    error_msg = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        error_msg = "Wrong format"
    if error_msg is None and request_json.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and request_json.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = request_json.get("email")
            user.password = request_json.get("password")
            user.first_name = request_json.get("first_name")
            user.last_name = request_json.get("last_name")
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
    request_json = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        return jsonify({'error': "Wrong format"}), 400
    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')
    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
