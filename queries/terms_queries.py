import graphene
from type.terms_type import TermsType
from model.terms_model import Terms

class TermsQueries(graphene.ObjectType):
    terms = graphene.List(TermsType)
    term = graphene.Field(TermsType, id=graphene.Int())
    
    def resolve_terms(self, info):
        return Terms.query.all()
    def resolve_term(self, info, id):
        return Terms.query.filter_by(id == id).first()