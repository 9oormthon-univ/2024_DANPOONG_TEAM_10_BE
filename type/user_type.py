from graphene_sqlalchemy import SQLAlchemyObjectType
from model.user_model import User
#DB 테이블 정의
class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User