import graphene
from flask import request
from db_config import db
from utils.auth import login_required
from type.user_festival_like_type import UserFestivalLikeType
from model.mapping.user_festival_like import UserFestivalLike
from model.user_model import User


class CreateUserFestivalLike(graphene.Mutation):
    class Arguments:
        festival_id=graphene.Int(required=True)
    success=graphene.Boolean()
    message = graphene.String()
    user_festival_like = graphene.Field(lambda:UserFestivalLikeType)
    
    @login_required
    def mutate(self, info, festival_id):
        try:
            if not festival_id:
                return CreateUserFestivalLike(
                    success=False,
                    message="축제 ID가 유효하지 않습니다."
                )
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user = User.query.filter(User.kakao_id == social_kakao_id).first()
            # 이미 좋아요 했는지 확인
            existed_like=UserFestivalLike.query.filter_by(user_id=user.id,festival_id=festival_id).first()
            if existed_like:
                return CreateUserFestivalLike(
                    success=False,
                    message="이미 좋아요 완료한 축제입니다",
                    user_festival_like=existed_like
                )
            new_like = UserFestivalLike(user_id=user.id, festival_id=festival_id)
            db.session.add(new_like)
            db.session.commit()
            
            return CreateUserFestivalLike(
                success=True,
                message="축제 좋아요 처리가 완료되었습니다.",
                user_festival_like=new_like
            )
            
        except Exception as e:
            db.session.rollback()
            return CreateUserFestivalLike(
                success=False,
                message=f"축제 좋아요 처리 중 오류가 발생했습니다.: {str(e)}"
            )
class DeleteUserFestivalLike(graphene.Mutation):
    class Arguments:
        festival_id=graphene.Int(required=True)
    success=graphene.Boolean()
    message = graphene.String()
    
    @login_required
    def mutate(self, info, festival_id):
        try:
            if not festival_id:
                return CreateUserFestivalLike(
                    success=False,
                    message="축제 ID가 유효하지 않습니다."
                )
            user_info = request.user
            social_kakao_id = str(user_info["id"])
            user = User.query.filter(User.kakao_id == social_kakao_id).first()
            # 이미 좋아요 했는지 확인
            existed_like=UserFestivalLike.query.filter_by(user_id=user.id,festival_id=festival_id).first()
            if not existed_like:
                return DeleteUserFestivalLike(
                    success=False,
                    message="이미 좋아요 내역에 없습니다.",
                )
            db.session.delete(existed_like)
            db.session.commit()
            
            return DeleteUserFestivalLike(
                success=True,
                message="축제 좋아요 삭제 처리가 완료되었습니다.",
            )
            
        except Exception as e:
            db.session.rollback()
            return DeleteUserFestivalLike(
                success=False,
                message=f"축제 좋아요 삭제 중 오류가 발생했습니다.: {str(e)}"
            )
class UserFestivalLikeMutations(graphene.ObjectType):
    create_user_festival_like = CreateUserFestivalLike.Field()
    delete_user_festival_like=DeleteUserFestivalLike.Field()