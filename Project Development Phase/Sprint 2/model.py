from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin

class user(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    
class student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    place=db.Column(db.String, nullable=False)
    number=db.Column(db.String, nullable=False)
    occupation=db.Column(db.String, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey(user.id), nullable=False, )


