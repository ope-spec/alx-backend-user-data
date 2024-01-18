#!/usr/bin/env python3
"""
Base module for managing objects
"""

from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base():
    """
    Base class for object management
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a Base instance.
        """
        selfClass = str(self.__class__.__name__)
        if DATA.get(selfClass) is None:
            DATA[selfClass] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = datetime.strptime(
            kwargs.get('created_at',
                       datetime.utcnow().strftime(TIMESTAMP_FORMAT)),
            TIMESTAMP_FORMAT
        )
        self.updated_at = datetime.strptime(
            kwargs.get('updated_at',
                       datetime.utcnow().strftime(TIMESTAMP_FORMAT)),
            TIMESTAMP_FORMAT
        )

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """
        Check equality between two Base objects.
        """
        if type(self) is not type(other):
            return False
            if not isinstance(self, Base):
                return False
                return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """
        Convert the object to a JSON dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """
        Load all objects from file.
        """
        selfClass = cls.__name__
        file_path = f".db_{selfClass}.json"
        DATA[selfClass] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[selfClass][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """
        Save all objects to file.
        """
        selfClass = cls.__name__
        file_path = f".db_{selfClass}.json"
        objs_json = {
            obj_id: obj.to_json(True) for obj_id,
            obj in DATA[selfClass].items()
            }

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """
        Save the current object to the data storage.
        """
        selfClass = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[selfClass][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """
        Removes object.
        """
        selfClass = self.__class__.__name__
        if DATA[selfClass].get(self.id) is not None:
            del DATA[selfClass][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """
        Count the total number of objects in the data storage.
        """
        selfClass = cls.__name__
        return len(DATA[selfClass])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """
        Retrieve all objects from the data storage.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """
        Retrieve one object by its unique ID from the data storage.
        """
        selfClass = cls.__name__
        return DATA[selfClass].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """
        Search for objects in the data storage with matching attributes.
        """
        selfClass = cls.__name__

        def _search(obj):
            if not attributes:
                return True
            return all(getattr(obj, k) == v for k, v in attributes.items())

        return list(filter(_search, DATA[selfClass].values()))
