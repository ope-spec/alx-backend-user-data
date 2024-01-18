#!/usr/bin/env python3
"""
Main module for the API Routes
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Filter each request before sending it to the appropriate route.
    """
    if auth is not None:
        setattr(request, "current_user", auth.current_user(request))
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            cookie = auth.session_cookie(request)
            if auth_header is None and cookie is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found_handler(error) -> str:
    """
    Handler for Not Found errors.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_handler(error) -> str:
    """
    Checks for Unauthorized errors.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_handler(error) -> str:
    """
    checks for Forbidden errors.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
