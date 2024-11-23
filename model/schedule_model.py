from sqlalchemy import BigInteger, Time, String, Text
from model.base_model import BaseTable, db

class Schedule(BaseTable):
    """O스케줄의 각 이벤트 모델"""
    
    __tablename__ = 'schedule'

    order = db.Column(db.Integer, nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    festival_id = db.Column(db.Integer, db.ForeignKey('festival.id'), nullable=False)
    start_time = db.Column(db.Time, nullable=True)
    name = db.Column(String(255), nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint('order', 'event_date', 'festival_id'),
    )