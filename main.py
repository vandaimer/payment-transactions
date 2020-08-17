import logging

import app as application
from db import db_connection

def init():
    try:
        db_connection.test_connection()
        db_connection.create_tables()
    except Exception as e:
        logging.error(e)
        raise e

    return application.start()

app = init()
