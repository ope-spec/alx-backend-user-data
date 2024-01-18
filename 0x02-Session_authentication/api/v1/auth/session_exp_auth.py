#!/usr/bin/env python3
"""
Definition of SessionExpAuth class with added expiration date for Session ID
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class adds an expiration date to a Session ID
    """

    def __init__(self):
        """
        Initialize the class with session duration from environment variable
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Create a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_details = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_details
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None or "created_at" not in user_details:
            return None
        if self.session_duration > 0:
            created_at = user_details["created_at"]
            allowed_window = created_at + timedelta(
                seconds=self.session_duration)
            if allowed_window < datetime.now():
                return None
        return user_details.get("user_id")
