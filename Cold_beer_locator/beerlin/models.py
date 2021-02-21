from datetime import datetime
from beerlin import db, login_manager
from flask_login import UserMixin
from sqlalchemy import func, ForeignKeyConstraint
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# test_table = db.Table('test_table', db.Model.metadata,
#     db.Column('left_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('right_id', db.Integer, db.ForeignKey('post.id'))
# )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', foreign_keys='[post.id]',backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Local(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    name= db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"['{self.name}', {self.latitude}, {self.longitude}]"



