from model.base_model import BaseTable
from db_config import db

class UserFestivalLike(BaseTable):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    festival_id = db.Column(db.Integer, db.ForeignKey('festival.id'), nullable=False)
    def __init__(self, user_id, festival_id):
        self.user_id = user_id
        self.festival_id = festival_id
