import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from model.user_model import User
from model.terms_model import Terms
from model.mapping.user_agree_model import UserAgree
from model.mapping.review_model import Review
from model.festival_model import Festival
from db_config import db
from utils.auth import login_required
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
class ReviewType(SQLAlchemyObjectType):
    class Meta:
        model = Review
class FestivalType(SQLAlchemyObjectType):
    class Meta:
        model = Festival

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, kakao_id=graphene.String())
    user_agrees=graphene.List(UserAgreeType)
    user_agree=graphene.Field(UserAgreeType,terms_id=graphene.Int())
    terms = graphene.List(TermsType)
    term = graphene.Field(TermsType, id=graphene.Int())
    reviews=graphene.List(ReviewType,festival_id=graphene.Int(),user_id=graphene.Int())
    review=graphene.Field(ReviewType,user_id=graphene.Int())
    festivals = graphene.List(FestivalType)
    festival = graphene.Field(FestivalType, id=graphene.Int())
    
    def resolve_users(self, info):
        return User.query.all()
    def resolve_user(self, info, kakao_id):
        return User.query.filter_by(kakao_id = kakao_id).first()
    def resolve_user_agree(self, info, terms_id):
        return UserAgree.query.filter_by(terms_id=terms_id).first()
    def resolve_terms(self, info):
        return Terms.query.all()
    def resolve_term(self, info, id):
        return Terms.query.filter_by(id == id).first()
    def resolve_reviews(self, info,festival_id=None, user_id=None):
        query=Review.query
        if festival_id:
            query = query.filter_by(festival_id = festival_id)
        if user_id:
            query = query.filter_by(user_id = user_id)
        return query.all()
    def resolve_review(self, info, user_id=None):
        if user_id is None:
            return None
        return Review.query.filter_by(user_id == user_id).first()
    def resolve_festivals(self, info):
        return Festival.query.all()
    def resolve_festival(self, info, id):
        return Festival.query.filter_by(id=id).first()

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
            message="��로필이 성공적으로 업데이트되었습니다"
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
class CreateReview(graphene.Mutation):
    class Arguments:
        festival_id = graphene.Int(required=True)
        body = graphene.String(required=True)
        score = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    review = graphene.Field(ReviewType)

    @login_required
    def mutate(self, info, festival_id,body,score):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user=User.query.filter(User.kakao_id == social_kakao_id).first()
            new_review=Review(user_id=user.id, festival_id=festival_id,body=body,score=score)
            db.session.add(new_review)
            db.session.commit()
            return CreateReview(
                success=True,
                message="리뷰 등록이 완료되었습니다.",
                review=new_review
            )
        except Exception as e:
            db.session.rollback()
            return CreateReview(
                success=False,
                message=f"리뷰 등록 중 오류가 발생했습니다: {str(e)}"
            )
class DeleteReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    review=graphene.Field(ReviewType)

    @login_required
    def mutate(self, info, review_id):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user=User.query.filter(User.kakao_id == social_kakao_id).first()
            #먼저 DB에서 리뷰를 찾음
            review=Review.query.get(review_id)
            if not review:
                return DeleteReview(
                    success=False,
                    message="리뷰를 찾을 수 없습니다."
                )
            
            #리뷰 작성자가 다른경우
            if review.user_id!=user.id:
                return DeleteReview(
                    success=False,
                    message="자신이 작성한 리뷰만 삭제할 수 있습니다."
                )
            db.session.delete(review)
            db.session.commit()
            return DeleteReview(
                success=True,
                message="리뷰가 성공적으로 삭제되었습니다."
            )
        except Exception as e:
            db.session.rollback()
            return DeleteReview(
                success=False,
                message=f"리뷰 삭제 중 오류가 발생했습니다: {str(e)}"
            )
class UpdateReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.Int(required=True)
        body = graphene.String(required=True)
        score = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    review = graphene.Field(ReviewType)

    @login_required
    def mutate(self, info, review_id,body,score):
        try:
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user=User.query.filter(User.kakao_id == social_kakao_id).first()
            #먼저 DB에서 리뷰를 찾음
            review=Review.query.get(review_id)
            if not review:
                return UpdateReview(
                    success=False,
                    message="리뷰를 찾을 수 없습니다."
                )
            #리뷰 작성자가 다른경우
            if review.user_id!=user.id:
                return UpdateReview(
                    success=False,
                    message="자신이 작성한 리뷰만 수정할 수 있습니다."
                )
            review.body=body
            review.score=score
            db.session.commit()
            return UpdateReview(
                success=True,
                message="리뷰가 성공적으로 수정되었습니다.",
                review=review
            )
        except Exception as e:
            db.session.rollback()
            return UpdateReview(
                success=False,
                message=f"리뷰 수정 중 오류가 발생했습니다: {str(e)}"
            )
class CreateFestival(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        created_at = graphene.String(required=True)
        updated_at = graphene.String(required=True)

    festival = graphene.Field(lambda: FestivalType)

    def mutate(self, info, name, created_at, updated_at):
        festival = Festival(name=name, created_at=created_at, updated_at=updated_at)
        db.session.add(festival)
        db.session.commit()
        return CreateFestival(festival=festival)
                
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()  # Mutation 등록
    agree_to_terms = AgreeToTerms.Field()
    create_review = CreateReview.Field()
    update_review=UpdateReview.Field()
    delete_review=DeleteReview.Field()
    create_festival = CreateFestival.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
