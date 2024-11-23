import graphene
from type.user_type import UserType
from model.user_model import User

class UserQueries(graphene.ObjectType):
    users = graphene.List(UserType)
    #TODO: 추후 ID 기준으로 변경
    user = graphene.Field(
        UserType, 
        kakao_id=graphene.String(),
        description="kakao_id로 user 탐색")

    def resolve_users(self, info):
        return User.query.all()

    def resolve_user(self, info, kakao_id):
        return User.query.filter_by(kakao_id=kakao_id).first()