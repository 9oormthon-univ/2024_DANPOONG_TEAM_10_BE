import graphene
from graphql import GraphQLError
from type.chat_log_type import ChatLogType
from model.user_chat_log_model import UserChatLog

class UserChatQueries(graphene.ObjectType):
    chat_logs=graphene.Field(ChatLogType,festival_id=graphene.Int(required=True),user_id=graphene.Int(required=True)
                            ,description="해당 유저가 입장한 축제 채팅방의 입퇴장 로그를 반환")
    
    def resolve_chatlogs(self, info,festival_id, user_id):
        if not festival_id or not user_id:
            raise GraphQLError("festival_id와 user_id는 필수 파라미터입니다.")
        # 해당 유저의 입장 시간 조회
        entered_chat_log=UserChatLog.query.filter_by(
            festival_id=festival_id,
            user_id=user_id
        ).first()
        if not entered_chat_log:
            raise GraphQLError("해당 유저의 채팅방 입장 기록이 없습니다.")
        return entered_chat_log