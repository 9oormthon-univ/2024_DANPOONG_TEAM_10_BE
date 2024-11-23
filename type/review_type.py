from graphene_sqlalchemy import SQLAlchemyObjectType
from model.mapping.review_model import Review

class ReviewType(SQLAlchemyObjectType):
    class Meta:
        model=Review