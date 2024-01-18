#!/usr/bin/env python3
"""
Definition of class BasicAuth implementing
Basic Authorization protocol methods
"""

import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Implement Basic Authorization protocol methods
    """

    def extract_base64_authorization_header(self,
                                            authorization_header:
                                            str) -> str:
        """
        This extracts the Base64 part of the
        Authorization header for Basic Authorization.
        """
        if not authorization_header or \
                not isinstance(authorization_header, str) \
                or not authorization_header.startswith("Basic "):
            return None
        token = authorization_header.split(" ")[-1]
        return token

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        This decodes a Base64-encoded string.
        """
        if not base64_authorization_header or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header.encode('utf-8')
            ).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns user email and password from Base64 decoded value.
        """
        if not decoded_base64_authorization_header or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Return a User instance based on email and password.
        """
        if not user_email or not isinstance(user_email, str) or \
                not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a received request.
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, pword = self.extract_user_credentials(decoded)
                    if email:
                        return self.user_object_from_credentials(email, pword)
        return None
