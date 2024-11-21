from flask import Blueprint, jsonify, request

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    # 요청에서 사용자 입력 가져오기
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # 인증 로직
    if username == "admin" and password == "password":  # 예: 하드코딩된 인증
        # 성공 시 토큰 반환 (JWT 등 사용 가능)
        return jsonify({"message": "Login successful", "token": "your_token_here"}), 200
    else:
        # 실패 시 에러 메시지 반환
        return jsonify({"message": "Invalid credentials"}), 401