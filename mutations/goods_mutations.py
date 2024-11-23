import graphene
from flask import request
from db_config import db
from utils.auth import login_required
from model.mapping.goods_model import Goods
from type.goods_type import GoodsType
from model.user_model import User

class CreateGoods(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    goods = graphene.Field(GoodsType)

    @login_required
    def mutate(self, info, festival_id,body,score):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user=User.query.filter(User.kakao_id == social_kakao_id).first()
            new_goods=Goods(user_id=user.id, festival_id=festival_id,body=body,score=score)
            db.session.add(new_goods)
            db.session.commit()
            return CreateGoods(
                success=True,
                message="굿즈 수령이 완료되었습니다.",
                goods=new_goods
            )
        except Exception as e:
            db.session.rollback()
            return CreateGoods(
                success=False,
                message=f"굿즈 수령 체크중 오류 발생: {str(e)}"
            )
class GoodsMutations(graphene.ObjectType):
    create_goods= CreateGoods.Field(description="사용자가 해당 지역구의 3회 리뷰 남길 경우 이것을 실행")