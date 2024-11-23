import graphene
from type.festival_type import FestivalType
from model.festival_model import Festival

class FestivalQueries(graphene.ObjectType):
    festivals = graphene.List(FestivalType)
    festival = graphene.Field(FestivalType, contentid=graphene.String())

    def resolve_users(self, info):
        return Festival.query.all()

    def resolve_user(self, info, contentid):
        return Festival.query.filter_by(contentid=contentid).first()