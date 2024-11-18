from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#id:admin pw:admin
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/passionpay_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "DB연결 성공"

if __name__ == '__main__':
    app.run(debug=True)