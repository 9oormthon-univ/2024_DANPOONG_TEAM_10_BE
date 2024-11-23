import graphene
from type.chat_log_type import ChatLogType
from model.chat_log_model import ChatLog

class ChatLogQueries(graphene.ObjectType):
    chat_logs=graphene.List(ChatLogType,festival_id=graphene.Int(required=True),user_id=graphene.Int(required=True)
                            ,description="해당 유저가 입장한 축제 채팅방의 입장시간 이후의 채팅들을 반환")
    
    def resolve_chatlogs(self, info,festival_id, user_id):
        if not festival_id or not user_id:
            raise GraphQLError("festival_id와 user_id는 필수 파라미터입니다.")
        query=ChatLog.query
        # 해당 유저의 입장 시간 조회
        entered_chat_log=UserChatLog.query.filter_by(
            festival_id=festival_id,
            user_id=user_id
        ).first()
        if not entered_chat_log:
            raise GraphQLError("해당 유저의 채팅방 입장 기록이 없습니다.")
        query=query.filter(
            ChatLog.festival_id == festival_id,
            ChatLog.created_at >= entered_chat_log.enter_time
        )
        return query.order_by(ChatLog.created_at).all()