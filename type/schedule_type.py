from graphene_sqlalchemy import SQLAlchemyObjectType
from model.schedule_model import Schedule

class ScheduleType(SQLAlchemyObjectType):
    class Meta:
        model=Schedule