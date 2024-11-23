import graphene
from flask import request
from db_config import db
from utils.auth import login_required
from type.user_agree_type import UserAgreeType
from model.terms_model import Terms
from model.user_model import User
from model.mapping.user_agree_model import UserAgree

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
class UserAgreeMutations(graphene.ObjectType):
    agree_to_terms = AgreeToTerms.Field(description="현재 사용자의 해당 Term에 대한 동의 정보를 추가합니다.")