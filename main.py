from app import start
from db import DB

db = DB()
app = start(db)
