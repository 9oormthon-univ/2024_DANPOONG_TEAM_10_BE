from .base_model import BaseTable
from ..db_config import db


# db = SQLAlchemy()

class Terms(BaseTable):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(10), nullable=True)
    link = db.Column(db.Text, nullable=True)
    optional = db.Column(db.Boolean,unique=True)

    def __repr__(self):
        return f'<Terms {self.title}>'