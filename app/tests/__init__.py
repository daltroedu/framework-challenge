import unittest

from app import create_app
from app.ext.database.flask_sqlalchemy import db
from app.blueprints.models import Album, Comment, Post, User


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def headers(self):
        return {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def create_user(self):
        user = User('admin@example.com', 'admin', 'admin', 'Admin')
        db.session.add(user)
        db.session.commit()
        return user

    def create_album(self):
        user = self.create_user()
        album = Album(user.id, 'My Album', '')
        db.session.add(album)
        db.session.commit()
        return album

    def create_post(self):
        user = self.create_user()
        post = Post(user.id, 'My Post', 'Contents')
        db.session.add(post)
        db.session.commit()
        return post

    def create_comment(self):
        post = self.create_post()
        comment = Comment(1, post.id, 'My Comment')
        db.session.add(comment)
        db.session.commit()
        return comment