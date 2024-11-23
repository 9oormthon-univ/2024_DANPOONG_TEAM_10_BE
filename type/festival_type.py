from graphene_sqlalchemy import SQLAlchemyObjectType
from model.festival_model import Festival
#DB 테이블 정의
class FestivalType(SQLAlchemyObjectType):
    class Meta:
        model = Festival