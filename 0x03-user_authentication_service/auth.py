#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
import uuid
from uuid import uuid4
from user import User
from typing import TypeVar
from typing import TypeVar, Union
from sqlalchemy.orm.exc import NoResultFound


U = TypeVar('U', bound=User)


def _hash_password(password: str) -> bytes:
    """
    Hash a password string and return it in bytes form.
    """
    passwd = password.encode('utf-8')
    salted_hash = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return salted_hash


def _generate_uuid() -> str:
    """
    Generates UUID and return its string representation.
    """
    return str(uuid4())


class Auth:
    """
    Authentication Interface
    """

    def __init__(self) -> None:
        """
        Initialize a new instance of the Authentication class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and return a user object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided login credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        userPass = user.hashed_password
        password = password.encode("utf-8")
        return bcrypt.checkpw(password, userPass)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session for the user and return the session ID.
        """
        try:
            new_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(new_user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Get the user corresponding to the session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the given user ID
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user and return it
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token
        """
        try:
            old_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(old_user.id,
                             hashed_password=hashed, reset_token=None)
