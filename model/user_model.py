from .base_model import BaseTable
from db_config import db


# db = SQLAlchemy()

class User(BaseTable):
    #TODO: UUID로 변경
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nickname = db.Column(db.String(10), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    kakao_id = db.Column(db.String(10),unique=True)
    gender=db.Column(db.String(10))

    def __init__(self, kakao_id):
        self.kakao_id=kakao_id
    def __repr__(self):
        return f'<User {self.kakao_id}>'