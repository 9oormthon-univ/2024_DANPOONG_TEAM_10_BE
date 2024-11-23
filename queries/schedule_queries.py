import graphene
from graphql import GraphQLError
from type.schedule_type import ScheduleType
from model.schedule_model import Schedule

class ScheduleQueries(graphene.ObjectType):
    schedules = graphene.List(
        ScheduleType,
        festival_id=graphene.Int(required=True),
        event_date=graphene.Date(),
        description="""축제의 스케줄 목록을 반환. event_date가 주어지면 해당 날짜의 스케줄만 반환

            예시 쿼리:
            # 축제의 모든 스케줄 조회
            query {
            schedules(festivalId: 1) {
                name
                startTime
                endTime
                description
            }
            }

            # 특정 날짜의 스케줄만 조회
            query {
            schedules(festivalId: 1, eventDate: 20240315) {
                name
                startTime
                endTime
                description
            }
            }
"""
    )
    
    def resolve_schedules(self, info, festival_id, event_date=None):
        if not festival_id:
            raise GraphQLError("festival_id는 필수 파라미터입니다.")
            
        query = Schedule.query.filter_by(festival_id=festival_id)
        
        if event_date:
            query = query.filter_by(event_date=event_date)
            
        return query.order_by(Schedule.event_date, Schedule.order).all()