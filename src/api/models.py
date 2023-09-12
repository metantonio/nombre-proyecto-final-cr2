from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    profile_image_url = db.Column(db.String(255), unique=False, nullable=True)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "profile_image_url": self.profile_image_url
            # do not serialize the password, its a security breach
        }

class TokenBlocked(db.Model):
    __tablename__ = "tokenblocked"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "token": self.token,
            "date": self.date
            # do not serialize the password, its a security breach
        }

