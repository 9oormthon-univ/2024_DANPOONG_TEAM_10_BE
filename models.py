from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Festival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address1 = db.Column(db.String(200), nullable=False)
    address2 = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    photo1 = db.Column(db.String(200), nullable=True)
    photo2 = db.Column(db.String(200), nullable=True)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Festival {self.name}>'