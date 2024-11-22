from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#나중에 실제 서버 배포할 때는 이 부분을 환경변수 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)