from functools import wraps
from flask import request
from ..kakao_controller import Oauth

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {
                "status": 401,
                "message": "로그인이 필요합니다.",
                "result": "fail"
            }, 401
        try:
            # Bearer 토큰 형식 검증
            token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
                
            # 카카오 API로 토큰 유효성 검증
            oauth = Oauth()
            user_info = oauth.userinfo(token)
            print(user_info)
            # 요청에 사용자 정보 추가
            request.user = user_info
            return f(*args, **kwargs)
            
        except Exception:
            return {
                "status": 401,
                "message": "유효하지 않은 토큰입니다.",
                "result": "fail"
            }, 401
            
    return decorated_function 