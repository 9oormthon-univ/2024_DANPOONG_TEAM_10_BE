from graphene_sqlalchemy import SQLAlchemyObjectType
from model.terms_model import Terms

class TermsType(SQLAlchemyObjectType):
    class Meta:
        model=Terms