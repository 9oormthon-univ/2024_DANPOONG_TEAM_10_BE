import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .model.user_model import User
from .model.terms_model import Terms
from .model.mapping.user_agree_model import UserAgree
from .db_config import db
from.utils.auth import login_required
from flask import request
from datetime import datetime
#DB 테이블 정의
class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
class UserAgreeType(SQLAlchemyObjectType):
    class Meta:
        model = UserAgree
class TermsType(SQLAlchemyObjectType):
    class Meta:
        model = Terms

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, kakao_id=graphene.String())
    user_agrees=graphene.List(UserAgreeType)
    user_agree=graphene.Field(UserAgreeType,terms_id=graphene.Int())
    terms = graphene.List(TermsType)
    term = graphene.Field(TermsType, id=graphene.Int())
    
    def resolve_users(self, info):
        return User.query.all()
    def resolve_user(self, info, kakao_id):
        return User.query.filter(User.kakao_id == kakao_id).first()
    def resolve_user_agree(self, info, terms_id):
        return UserAgree.query.filter_by(terms_id=terms_id).first()
    def resolve_terms(self, info):
        return Terms.query.all()
    def resolve_term(self, info, id):
        return Terms.query.filter(Terms.id == id).first()

class CreateUser(graphene.Mutation):
    class Arguments:
        kakao_id=graphene.Int(required=True)
        
    user=graphene.Field(lambda:UserType)
    
    def mutate(self, info, kakao_id):
        user = User(kakao_id=kakao_id)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)
    
class UpdateProfile(graphene.Mutation):
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
            return UpdateProfile(
                success=False,
                message="닉네임은 1-10자 사이여야 합니다.",
                user=None
            )
        existing_user=User.query.filter(
            User.nickname==nickname,
            User.kakao_id!=social_kakao_id
        ).first()
        if(existing_user):
            return UpdateProfile(
                success=False,
                message="이미 사용 중인 닉네임입니다.",
                user=None
            )
            
            # 생년월일 유효성 검사
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            return UpdateProfile(
                success=False,
                message="올바른 생년월일 형식이 아닙니다 (YYYY-MM-DD)",
                user=None
            )
            
        # 성별 유효성 검사
        if gender not in ['female', 'male', 'none']:
            return UpdateProfile(
                success=False,
                message="올바른 성별을 선택해주세요",
                user=None
            )
        
        # 프로필 업데이트
        user.nickname = nickname
        user.birth_date = birth_date
        user.gender = gender
        db.session.commit()
        return UpdateProfile(
            user=user,
            message="프로필이 성공적으로 업데이트되었습니다"
        )
class AgreeToTerms(graphene.Mutation):
    class Arguments:
        terms_ids = graphene.List(graphene.Int, required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    user_agrees = graphene.List(UserAgreeType)
    
    @login_required
    def mutate(self, info, terms_ids):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user = User.query.filter(User.kakao_id == social_kakao_id).first()
            # 필수 약관이 모두 포함되어 있는지 확인
            required_terms = Terms.query.filter_by(optional=False).all()
            required_terms_ids = [term.id for term in required_terms]
            for required_id in required_terms_ids:
                if required_id not in terms_ids:
                    return AgreeToTerms(
                        success=False,
                        message="필수 약관에 모두 동의해주세요."
                    )
            # 약관 동의 처리
            user_agrees = []
            for terms_id in terms_ids:
                # 이미 동의한 약관인지 확인
                existing_agree = UserAgree.query.filter_by(
                    user_id=user.id,
                    terms_id=terms_id
                ).first()
                
                if not existing_agree:
                    new_agree = UserAgree(user_id=user.id, terms_id=terms_id)
                    db.session.add(new_agree)
                    db.session.flush()  # 각 항목마다 flush 추가
                    user_agrees.append(new_agree)
            
            db.session.commit()
            
            return AgreeToTerms(
                success=True,
                message="약관 동의가 완료되었습니다.",
                user_agrees=user_agrees
            )
            
        except Exception as e:
            db.session.rollback()
            return AgreeToTerms(
                success=False,
                message=f"약관 동의 처리 중 오류가 발생했습니다: {str(e)}"
            )
                
class Mutation(graphene.ObjectType):
    
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()  # Mutation 등록
    agree_to_terms = AgreeToTerms.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
