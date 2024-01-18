#!/usr/bin/env python3
"""
Module for managing user sessions.
"""

from models.base import Base


class UserSession(Base):
    """
    User session class for storing session information.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance.

        Args:
            *args (list): Additional positional arguments.
            **kwargs (dict): Additional keyword arguments.
                user_id (str): User ID associated with the session.
                session_id (str): Session ID for the user.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
