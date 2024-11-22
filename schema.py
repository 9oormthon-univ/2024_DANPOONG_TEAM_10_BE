import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel, Festival as FestivalModel
from config import db

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Festival(SQLAlchemyObjectType):
    class Meta:
        model = FestivalModel

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, username, email):
        user = UserModel(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class CreateFestival(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address1 = graphene.String(required=True)
        address2 = graphene.String()
        phone = graphene.String()
        photo1 = graphene.String()
        photo2 = graphene.String()
        x_coordinate = graphene.Float(required=True)
        y_coordinate = graphene.Float(required=True)

    festival = graphene.Field(lambda: Festival)

    def mutate(self, info, name, address1, x_coordinate, y_coordinate, address2=None, phone=None, photo1=None, photo2=None):
        festival = FestivalModel(
            name=name,
            address1=address1,
            address2=address2,
            phone=phone,
            photo1=photo1,
            photo2=photo2,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate
        )
        db.session.add(festival)
        db.session.commit()
        return CreateFestival(festival=festival)

class FestivalConnection(graphene.Connection):
    class Meta:
        node = Festival

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int(required=True))
    festivals = graphene.ConnectionField(FestivalConnection)
    festival = graphene.Field(Festival, id=graphene.Int(required=True))

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_user(self, info, id):
        query = User.get_query(info)
        return query.get(id)

    def resolve_festivals(self, info, **args):
        query = Festival.get_query(info)
        return query.all()

    def resolve_festival(self, info, id):
        query = Festival.get_query(info)
        return query.get(id)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_festival = CreateFestival.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Festival])