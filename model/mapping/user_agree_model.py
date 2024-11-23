from model.base_model import BaseTable
from db_config import db


# db = SQLAlchemy()

class UserAgree(BaseTable):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    terms_id=db.Column(db.Integer,db.ForeignKey('terms.id'),nullable=False)
    def __init__(self, user_id, terms_id):
        self.user_id = user_id
        self.terms_id = terms_id
    