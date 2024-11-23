import graphene
from type.user_agree_type import UserAgreeType
from model.mapping.user_agree_model import UserAgree

class UserAgreeQueries(graphene.ObjectType):
    user_agrees=graphene.List(UserAgreeType)
    user_agree=graphene.Field(UserAgreeType,terms_id=graphene.Int())
    
    def resolve_user_agree(self, info, terms_id):
        return UserAgree.query.filter_by(terms_id=terms_id).first()