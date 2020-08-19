import logging

import app as application
from db import db_connection

log = logging.getLogger(__name__)


def init():
    try:
        db_connection.test_connection()
        db_connection.create_tables()
    except Exception as e:
        log.error(e)
        raise e

    return application.start()


app = init()
