from .base_model import BaseTable
from ...db_config import db


# db = SQLAlchemy()

class UserAgree(BaseTable):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'),nullable=False)
    terms_id=db.Column(db.Integer,db.ForeignKey('terms.id'),nullable=False)
    def __init__(self, kakao_id):
        self.kakao_id=kakao_id
    