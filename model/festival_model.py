from model.base_model import BaseTable
from db_config import db

class Festival(BaseTable):
    __tablename__ = 'festival'
    
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name=db.Column(db.String(100), nullable=False)  # 축제 이름