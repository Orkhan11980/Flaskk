from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Text
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favori_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256))
    posts = db.relationship('Posts', backref='poster')
