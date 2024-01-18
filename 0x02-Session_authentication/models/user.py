#!/usr/bin/env python3
"""
Module for managing user information.
"""

from models.base import Base
import hashlib


class User(Base):
    """
    User class for storing user details.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a User instance.

        Args:
            *args (list): Additional positional arguments.
            **kwargs (dict): Additional keyword arguments.
                email (str): User's email address.
                _password (str): Encrypted password.
                first_name (str): User's first name.
                last_name (str): User's last name.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """
        Get the encrypted password.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """
        Set a new password and encrypt it
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """
        Validates password.
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """
        Display the user's name based on email/first_name/last_name.

        Returns:
            str: User's display name.
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
