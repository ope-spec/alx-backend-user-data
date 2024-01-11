#!/usr/bin/env python3
"""
Module for filtering sensitive information from log messages.
"""
import re
import logging
from typing import List
import csv
import os
import mysql.connector
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data INFO %(asctime)-15s: %(message)s"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, ';')
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields, redaction, message, separator):
    """Obfuscates sensitive information from a log message."""
    pattern = r'(?<=' + separator + '|^)(' + '|'.join(fields) + \
        ')=.*?(?=' + separator + '|$)'
    return re.sub(pattern, '\\1=' + redaction, message)


def get_db():
    """Return a connector to the MySQL database."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=dbname
    )

    return connection


def main():
    """
    Retrieve all rows in the users table and display
    each row under a filtered format.
    """

    PII_FIELDS = ["name", "email", "phone", "ssn",
                  "password", "ip", "last_login", "user_agent"]

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor.fetchall():
        log_msg = '; '.join(f"{field}={value}" for field,
                            value in zip(PII_FIELDS, row))
        logger.info(log_msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
