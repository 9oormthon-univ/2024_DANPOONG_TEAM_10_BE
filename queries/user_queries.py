import graphene
from type.user_type import UserType
from model.user_model import User

class UserQueries(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, kakao_id=graphene.String())

    def resolve_users(self, info):
        return User.query.all()

    def resolve_user(self, info, kakao_id):
        return User.query.filter_by(kakao_id=kakao_id).first()