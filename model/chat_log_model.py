from model.base_model import BaseTable
from db_config import db

class ChatLog(BaseTable):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    festival_id=db.Column(db.Integer,db.ForeignKey('festival.id'),nullable=False)
    body=db.Column(db.Text)
