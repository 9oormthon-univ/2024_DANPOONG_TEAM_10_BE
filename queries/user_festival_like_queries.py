import graphene
from graphql import GraphQLError
from flask import request
from type.user_festival_like_type import UserFestivalLikeType
from model.mapping.user_festival_like_model import UserFestivalLike
from utils.auth import login_required
from model.user_model import User

class UserFestivalLikeQueries(graphene.ObjectType):
    user_festival_likes=graphene.List(
        UserFestivalLikeType,
        user_id=graphene.Int(required=True),
        description="user Id의 축제 좋아요 목록을 반환합니다"
    )
    def resolve_user_festival_likes(self, info,user_id):
        if not user_id:
            raise GraphQLError("user_id는 필수 파라미터입니다.")
            
        likes = UserFestivalLike.query.filter_by(user_id=user_id).all()
        return likes