#!/usr/bin/env python3
"""
Implementation of SessionAuth class for Session Authorization protocol methods.
"""

import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    This class implements methods for the Session Authorization protocol.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user with the specified user_id.
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a session ID.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a user instance based on a cookie value.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Deletes a user session.
        """
        if not request:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
