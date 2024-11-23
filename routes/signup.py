from flask import Blueprint, request, redirect, session, jsonify
from flask_restx import Namespace, Resource, fields
from utils.auth import login_required
from kakao_controller import Oauth
from model.user_model import User
from db_config import db

# Blueprint 대신 Namespace 사용
signup = Namespace('signup', description='회원가입 관련 API')

# 요청 모델 정의
signup_model = signup.model('Signup', {
    'nickname': fields.String(required=True, description='사용자 이름',example="김철수"),
    'birth_date': fields.String(required=True, description='생년월일 (YYYY-MM-DD)',example="2001-03-24"),
    'gender': fields.String(required=True, description='성별 (male/female/none)',example="male")
})

# 응답 모델 정의
response_model = signup.model('Response', {
    'status': fields.Integer(description='상태 코드'),
    'message': fields.String(description='응답 메시지'),
    'result': fields.String(description='처리 결과')
})

@signup.route('/')
class SignupUser(Resource):
    @signup.doc(security='Bearer')
    @signup.expect(signup_model)
    @signup.response(200, '성공', response_model)
    @signup.response(400, '잘못된 요청', response_model)
    @signup.response(404, '사용자를 찾을 수 없음', response_model)
    @signup.response(500, '서버 에러', response_model)
    @login_required
    def post(self):
        """회원 정보 업데이트 API"""
        try:
            access_token = request.headers.get('Authorization')
            data = request.get_json()
            nickname = data.get('nickname')
            birth_date = data.get('birth_date')
            gender = data.get('gender')
            
            if not all([nickname, birth_date, gender, access_token]):
                return {
                    "status": 400,
                    "message": "필수 정보가 누락되었습니다.",
                    "result": "fail"
                }, 400
        
            oauth = Oauth()
            user = oauth.userinfo(access_token)
            social_kakao_id=str(user["id"])
            user_info = User.query.filter(User.kakao_id == social_kakao_id).first()
            
            if not user_info:
                return {
                    "status": 404,
                    "message": "사용자를 찾을 수 없습니다.",
                    "result": "fail"
                }, 404

            user_info.nickname = nickname
            user_info.birth_date = birth_date
            user_info.gender = gender
            
            db.session.commit()

            return {
                "status": 200,
                "message": "회원정보가 성공적으로 업데이트되었습니다.",
                "result": "success"
            }, 200

        except Exception as e:
            return {
                "status": 500,
                "message": f"서버 오류가 발생했습니다: {str(e)}",
                "result": "error"
            }, 500