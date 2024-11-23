from graphene_sqlalchemy import SQLAlchemyObjectType
from model.chat_log_model import ChatLog

class ChatLogType(SQLAlchemyObjectType):
    class Meta:
        model=ChatLog