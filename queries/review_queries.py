import graphene
from type.review_type import ReviewType
from model.mapping.review_model import Review

class ReviewQueries(graphene.ObjectType):
    reviews=graphene.List(ReviewType,festival_id=graphene.Int(),user_id=graphene.Int())
    review=graphene.Field(ReviewType,user_id=graphene.Int())
    
    def resolve_reviews(self, info,festival_id=None, user_id=None):
        query=Review.query
        if festival_id:
            query = query.filter_by(festival_id = festival_id)
        if user_id:
            query = query.filter_by(user_id = user_id)
        return query.all()
    def resolve_review(self, info, user_id=None):
        if user_id is None:
            return None
        return Review.query.filter_by(user_id == user_id).first()