import graphene
from type.goods_type import StampType
from model.mapping.goods_model import Stamp

class StampQueries(graphene.ObjectType):
    stamp=graphene.Field(StampType,user_id=graphene.Int(required=True),
                         description="유저가 획득한 스탬프 목록들을 반환")
    def resolve_stamp(self, info, user_id=None):
        if user_id is None:
            return None
        return Stamp.query.filter_by(user_id == user_id).first()