from model.base_model import BaseTable
from db_config import db

class UserChatLog(BaseTable):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    festival_id=db.Column(db.Integer,db.ForeignKey('festival.id'),nullable=False)
    entry_status=db.Column(db.Integer)