import graphene
from queries.user_queries import UserQueries
from queries.terms_queries import TermsQueries
from queries.review_queries import ReviewQueries
from queries.user_agree_queries import UserAgreeQueries
from queries.user_festival_like_queries import UserFestivalLikeQueries
from queries.stamp_queries import StampQueries
from queries.festival_queries import FestivalQueries
from mutations.user_mutations import UserMutations
from mutations.user_agree_mutations import UserAgreeMutations
from mutations.review_mutations import ReviewMutations
from mutations.user_festival_like_mutations import UserFestivalLikeMutations


class Query(FestivalQueries, UserQueries, TermsQueries, ReviewQueries,UserAgreeQueries,UserFestivalLikeQueries,StampQueries,graphene.ObjectType):
    pass

class Mutation(UserMutations, ReviewMutations,UserAgreeMutations, UserFestivalLikeMutations,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)