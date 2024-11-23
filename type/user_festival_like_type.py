from graphene_sqlalchemy import SQLAlchemyObjectType
from model.mapping.user_festival_like import UserFestivalLike

class UserFestivalLikeType(SQLAlchemyObjectType):
    class Meta:
        model=UserFestivalLike