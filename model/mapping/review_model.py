from model.base_model import BaseTable
from db_config import db


class Review(BaseTable):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    festival_id=db.Column(db.Integer,db.ForeignKey('festival.id'),nullable=False)
    body=db.Column(db.Text)
    score=db.Column(db.Integer)
    
    def __init__(self, user_id, festival_id,body,score):
        self.user_id = user_id
        self.festival_id = festival_id
        self.body=body
        self.score=score
    def __repr__(self):
        return f'<Review {self.id}: {self.score}점>'