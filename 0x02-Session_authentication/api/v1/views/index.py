#!/usr/bin/env python3
"""
Module for Index Views
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized',
                 methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    Returns 401 Unauthorized error.
    """
    abort(401, description="Unauthorized")


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """
    Returns 403 Forbidden error.
    """
    abort(403, description="Forbidden")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    Returns the number of each object type in the system.
    """
    from models.user import User
    stats = {'users': User.count()}
    return jsonify(stats)
