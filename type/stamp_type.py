from graphene_sqlalchemy import SQLAlchemyObjectType
from model.mapping.stamp_model import Stamp

class StampType(SQLAlchemyObjectType):
    class Meta:
        model = Stamp