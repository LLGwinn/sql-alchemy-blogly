from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)               
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default='no image available')

    post = db.relationship('Post', backref='users', passive_deletes=True)
    
    def __repr__(self):
        u = self
        return f'<User id:{u.id} Name:{u.full_name}>'

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    
class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')
    post_tags = db.relationship('PostTag', backref='post')

    def __repr__(self):
        p = self
        return f'<Post id:{p.id} Title:{p.title}>'

    @property
    def format_date(self):
        """ Return date in user-friendly format """

        return (self.created_at.strftime("%a %b %d %Y, %I:%M %p"))

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        t = self
        return f'<Tag id:{t.id} Name:{t.name}>'


class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        pt = self
        return f'<post_id:{pt.post_id} tag_id:{pt.tag_id}>'



