import graphene
from flask import request
from datetime import datetime
from db_config import db
from utils.auth import login_required
from type.user_type import UserType
from model.user_model import User

class CreateUser(graphene.Mutation):
    class Arguments:
        kakao_id=graphene.Int(required=True)
        
    user=graphene.Field(lambda:UserType)
    
    def mutate(self, info, kakao_id):
        user = User(kakao_id=kakao_id)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)
    
class UpdateUser(graphene.Mutation):
    class Arguments:
        nickname = graphene.String()
        birth_date = graphene.String()
        gender = graphene.String()
    
    user = graphene.Field(lambda: UserType)
    message = graphene.String()
    success = graphene.Boolean()
    
    @login_required
    def mutate(self, info, nickname, birth_date, gender):
        user_info = request.user
        social_kakao_id=str(user_info["id"])
        user = User.query.filter(User.kakao_id == social_kakao_id).first()

       # 닉네임 유효성 검사
        if not nickname or len(nickname) > 10:
            return UpdateUser(
                success=False,
                message="닉네임은 1-10자 사이여야 합니다.",
                user=None
            )
        existing_user=User.query.filter(
            User.nickname==nickname,
            User.kakao_id!=social_kakao_id
        ).first()
        if(existing_user):
            return UpdateUser(
                success=False,
                message="이미 사용 중인 닉네임입니다.",
                user=None
            )
            # 생년월일 유효성 검사
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            return UpdateUser(
                success=False,
                message="올바른 생년월일 형식이 아닙니다 (YYYY-MM-DD)",
                user=None
            )
            
        # 성별 유효성 검사
        if gender not in ['female', 'male', 'none']:
            return UpdateUser(
                success=False,
                message="올바른 성별을 선택해주세요",
                user=None
            )
        
        # 프로필 업데이트
        user.nickname = nickname
        user.birth_date = birth_date
        user.gender = gender
        db.session.commit()
        return UpdateUser(
            user=user,
            message="프로필이 성공적으로 업데이트되었습니다"
        )

class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field(description="토큰을 통해 kakao_id 기반으로 유저를 생성합니다")
    update_user = UpdateUser.Field(description="폼 기반으로 유저를 업데이트 합니다")