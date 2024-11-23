import graphene
from type.stamp_type import StampType
from model.mapping.stamp_model import Stamp

class StampQueries(graphene.ObjectType):
    stamp=graphene.Field(StampType,user_id=graphene.Int())
    
    def resolve_review(self, info, user_id=None):
        if user_id is None:
            return None
        return Stamp.query.filter_by(user_id == user_id).first()