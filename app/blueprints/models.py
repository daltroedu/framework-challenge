from datetime import datetime

from flask import url_for
from werkzeug.security import generate_password_hash

from app.ext.database.flask_sqlalchemy import db


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False, index=True)
    contents = db.Column(db.Text())
    images = db.relationship('AlbumImage', backref='album', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, title, contents):
        self.user_id = user_id
        self.title = title
        self.contents = contents

    def __repr__(self):
        return f'<Album {self.id}>'


class AlbumImage(db.Model):
    __tablename__ = 'albums_images'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'<AlbumImage {self.id}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False, index=True)
    contents = db.Column(db.Text(), nullable=False)
    images = db.relationship('PostImage', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, title, contents):
        self.user_id = user_id
        self.title = title
        self.contents = contents

    def __repr__(self):
        return f'<Post {self.id}>'


class PostImage(db.Model):
    __tablename__ = 'posts_images'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'<PostImage {self.id}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    contents = db.Column(db.Text(), nullable=False)

    def __init__(self, user_id, post_id, contents):        
        self.user_id = user_id
        self.post_id = post_id
        self.contents = contents

    def __repr__(self):
        return f'<Comment {self.id}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    albums = db.relationship('Album', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email, username, password, name):
        self.email = email
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f'<User {self.id}>'