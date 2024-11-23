import graphene
from graphql import GraphQLError
from type.user_agree_type import UserAgreeType
from model.mapping.user_agree_model import UserAgree

class UserAgreeQueries(graphene.ObjectType):
    user_agrees=graphene.List(UserAgreeType,
                               user_id=graphene.Int(required=True),
                                description="유저의 약관 동의 내역을 반환"
    )
    
    def resolve_user_agrees(self, info, user_id):
        if not user_id:
            raise GraphQLError("user_id는 필수 파라미터입니다.")
            
        agrees = UserAgree.query.filter_by(user_id=user_id).all()
        
        if not agrees:
            return []
            
        return agrees