from model.base_model import BaseTable
from db_config import db
from model.festival_model import Festival  # Festival 모델 import 추가
from model.user_model import User  # User 모델도 import 추가


class Goods(BaseTable):
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
    festival_id=db.Column(db.Integer,db.ForeignKey('festival.id'),nullable=False)
    is_received = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f'<Terms {self.title}>'