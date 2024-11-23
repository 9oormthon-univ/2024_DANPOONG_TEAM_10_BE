from flask import Flask, render_template
from flask_graphql import GraphQLView
from dotenv import load_dotenv
from flask_restx import Api
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send
import os
import sys

# 프로젝트 루트 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

app = Flask(__name__)
from schema import schema
from db_config import db
from oauth import kakao
from model.user_model import User  # 필요한 모델들을 여기서 임포트
from model.terms_model import Terms
from model.mapping.user_agree_model import UserAgree
from model.mapping.review_model import Review
from model.festival_model import Festival

# 가장 먼저 환경변수 로드
load_dotenv()

CORS(app)  # CORS 활성화
port = int(os.getenv('FLASK_RUN_PORT', '5001'))

file_path = app.root_path
complete_path = os.path.join(file_path, 'folder', 'file.txt')
# API 객체 생성
api = Api(app)
api.add_namespace(kakao, path='/oauth/kakao')

# #id:admin pw:admin
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_ADDRESS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# SocketIO 설정
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app, ping_timeout=1800, ping_interval=25)  # 30분(1800초) 타임아웃, 25초마다 ping

@app.route('/')
def index():
    return "DB연결 성공"

@app.route('/test-profile')
def test_profile():
    return render_template('test_profile.html')

@app.route('/test-chat')
def test_chat():
    return render_template('chat.html')

# GraphQL 뷰 추가
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # GraphiQL 인터페이스 활성화
    )
)

# WebSocket 이벤트 핸들러
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f'{username} has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f'{username} has left the room.', to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    send(data['message'], to=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=443)
    # app.run(debug=True, port=port)