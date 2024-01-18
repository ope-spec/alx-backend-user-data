#!/usr/bin/env python3
"""
Definition of class Auth for managing API authentication
"""

import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class for managing API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not.
        """
        if path is None:
            return True
        elif not excluded_paths or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if (
                    i.startswith(path) or
                    path.startswith(i) or
                    (i[-1] == "*" and path.startswith(i[:-1]))
                ):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object.
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie from a request.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
