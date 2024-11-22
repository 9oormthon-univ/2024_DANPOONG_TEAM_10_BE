from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
import os
from .routes.signup import signup
from .oauth import kakao
from .db_config import db

# 가장 먼저 환경변수 로드
load_dotenv()


app = Flask(__name__)
port = int(os.getenv('FLASK_RUN_PORT', '5001'))

# #id:admin pw:admin
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/passionpay_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# Swagger UI 설정
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app,
    version='1.0',
    title='회원가입 API',
    description='회원가입 관련 API 문서',
    authorizations=authorizations,
    security='Bearer'
)

api.add_namespace(kakao, path='/oauth/kakao')
api.add_namespace(signup, path='/signup')

@app.route('/')
def index():
    return "DB연결 성공"

if __name__ == '__main__':
    app.run(debug=True ,port=port)