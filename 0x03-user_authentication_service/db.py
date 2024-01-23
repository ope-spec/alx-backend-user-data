"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User

Base.metadata.bind = create_engine("sqlite:///a.db", echo=True)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the specified criteria
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound(
                    "No result found for the specified criteria")
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid request: {}".format(str(e)))
        finally:
            self._session.close()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on the provided arguments
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError("Invalid argument: {}".format(key))
            self._session.commit()
        except NoResultFound as e:
            raise NoResultFound(
                "No result found for user_id: {}".format(user_id))
        except IntegrityError as e:
            self._session.rollback()
            raise IntegrityError("Integrity error: {}".format(str(e)))
        finally:
            self._session.close()
