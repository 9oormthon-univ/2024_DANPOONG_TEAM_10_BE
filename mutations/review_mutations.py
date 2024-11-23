import graphene
from flask import request
from db_config import db
from utils.auth import login_required
from model.mapping.review_model import Review
from type.review_type import ReviewType
from model.user_model import User

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
class ReviewMutations(graphene.ObjectType):
    create_review= CreateReview.Field()
    update_review = UpdateReview.Field()
    delete_review= DeleteReview.Field()