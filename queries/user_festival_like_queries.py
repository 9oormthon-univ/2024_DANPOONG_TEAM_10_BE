import graphene
from flask import request
from type.user_festival_like_type import UserFestivalLikeType
from model.mapping.user_festival_like_model import UserFestivalLike
from utils.auth import login_required
from model.user_model import User

class UserFestivalLikeQueries(graphene.ObjectType):
    user_festival_likes=graphene.List(UserFestivalLikeType,
                                      description="현재 로그인한 사용자의 축제 좋아요 목록을 반환합니다")
    @login_required
    def resolve_user_festival_likes(self, info):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user = User.query.filter(User.kakao_id == social_kakao_id).first()

            if not user:
                return []

            return UserFestivalLike.query.filter_by(user_id=user.id).all()

        except Exception as e:
            print(f"유저가 좋아요한 페스티벌 조회에 실패했습니다.: {str(e)}")
            return []