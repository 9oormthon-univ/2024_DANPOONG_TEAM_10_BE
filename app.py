from flask import Flask,render_template
from flask_graphql import GraphQLView
from dotenv import load_dotenv
from flask_restx import Api
from flask_cors import CORS
from schema import schema
from db_config import db
from oauth import kakao
import os

# 가장 먼저 환경변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 활성화
port = int(os.getenv('FLASK_RUN_PORT', '5001'))

# API 객체 생성
api = Api(app)
api.add_namespace(kakao, path='/oauth/kakao')

# #id:admin pw:admin
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_ADDRESS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "DB연결 성공"

@app.route('/test-profile')
def test_profile():
    return render_template('test_profile.html')
# GraphQL 뷰 추가
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # GraphiQL 인터페이스 활성화
    )
)

if __name__ == '__main__':
    app.run(debug=True ,port=port)