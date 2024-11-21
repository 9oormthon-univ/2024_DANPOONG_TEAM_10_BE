from flask import request, redirect, session
from flask_restx import Namespace, Resource, fields
from .key.kakao_client import CLIENT_ID, REDIRECT_URI, SIGNOUT_REDIRECT_URI
from .kakao_controller import Oauth
from .dto.member_model import Member
from .db_config import db

kakao = Namespace('oauth/kakao', description='카카오 OAuth 인증 관련 API')

# 응답 모델 정의
auth_response = kakao.model('AuthResponse', {
    'status': fields.Integer(description='상태 코드'),
    'message': fields.String(description='응답 메시지'),
    'result': fields.String(description='처리 결과'),
    'access_token': fields.String(description='액세스 토큰', required=False)
})

@kakao.route('/')
class KakaoSignIn(Resource):
    @kakao.doc('카카오 로그인')
    def get(self):
        """카카오 로그인 페이지로 리다이렉트"""
        kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
        return redirect(kakao_oauth_url)

@kakao.route('/callback')
class KakaoCallback(Resource):
    @kakao.doc('카카오 콜백 처리')
    @kakao.response(200, '성공', auth_response)
    @kakao.response(404, '인증 실패', auth_response)
    @kakao.response(500, '서버 에러', auth_response)
    def get(self):
        """카카오 OAuth 콜백 처리"""
        try:
            code = request.args["code"]
            oauth = Oauth()
            auth_info = oauth.auth(code)
            if "error" in auth_info:
                return {
                    "status": 404,
                    "message": "인증 실패",
                    "result": "fail"
                }, 404

            member = oauth.userinfo("Bearer " + auth_info['access_token'])
            member_info = Member.query.filter(Member.kakao_id == member["id"]).first()
            if member_info is None:
                member_info = Member(member["id"])
                db.session.add(member_info)
                db.session.commit()
                
                return {
                    "status": 200,
                    "message": "회원가입이 완료되었습니다.",
                    "result": "success",
                    "access_token": auth_info['access_token']
                }, 200
            else:
                return {
                    "status": 200,
                    "message": "로그인에 성공하였습니다.",
                    "result": "success",
                    "access_token": auth_info['access_token']
                }, 200
                
        except Exception as e:
            return {
                "status": 500,
                "message": f"서버 오류가 발생했습니다: {str(e)}",
                "result": "error"
            }, 500

@kakao.route('/signout')
class KakaoSignOut(Resource):
    @kakao.doc('카카오 로그아웃')
    @kakao.response(200, '성공', auth_response)
    @kakao.response(404, '실패', auth_response)
    def get(self):
        """카카오 로그아웃"""
        kakao_oauth_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={SIGNOUT_REDIRECT_URI}"

        if session.get('email'):
            session.clear()
        else:
            pass
        return redirect(kakao_oauth_url)