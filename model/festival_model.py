from model.base_model import BaseTable
from db_config import db

class Festival(BaseTable):
    __tablename__ = 'festival'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True) 
    name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.String, nullable=True)
'''
    cat1 = db.Column(db.String, nullable=True)
    cat2 = db.Column(db.String, nullable=True)
    cat3 = db.Column(db.String, nullable=True)
    contentid = db.Column(db.Integer, primary_key=True, nullable=True)
    contenttypeid = db.Column(db.Integer, nullable=True)
    createdtime = db.Column(db.String, nullable=True)
    eventstartdate = db.Column(db.String, nullable=True)
    eventenddate = db.Column(db.String, nullable=True)
    firstimage = db.Column(db.String, nullable=True)
    firstimage2 = db.Column(db.String, nullable=True)
    cpyrhtDivCd = db.Column(db.String, nullable=True)
    mapx = db.Column(db.Float, nullable=True)
    mapy = db.Column(db.Float, nullable=True)
    mlevel = db.Column(db.Integer, nullable=True)
    modifiedtime = db.Column(db.String, nullable=True)
    sigungucode = db.Column(db.Integer, nullable=True)
    tel = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)# 축제 이름
'''