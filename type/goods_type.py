from graphene_sqlalchemy import SQLAlchemyObjectType
from model.mapping.goods_model import Goods

class GoodsType(SQLAlchemyObjectType):
    class Meta:
        model = Goods