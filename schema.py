import graphene
from queries.user_queries import UserQueries
from queries.terms_queries import TermsQueries
from queries.review_queries import ReviewQueries
from queries.user_agree_queries import UserAgreeQueries
from mutations.user_mutations import UserMutations
from mutations.user_agree_mutations import UserAgreeMutations
from mutations.review_mutations import ReviewMutations

class Query(UserQueries, TermsQueries, ReviewQueries,UserAgreeQueries ,graphene.ObjectType):
    pass

class Mutation(UserMutations, ReviewMutations,UserAgreeMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)