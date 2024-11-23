from graphene_sqlalchemy import SQLAlchemyObjectType
from model.mapping.user_agree_model import UserAgree

class UserAgreeType(SQLAlchemyObjectType):
    class Meta:
        model = UserAgree