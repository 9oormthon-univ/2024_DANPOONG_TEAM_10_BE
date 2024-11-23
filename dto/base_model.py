import datetime
from ..db_config import db


class BaseTable(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())