"""SQLAlchemy models for blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all,delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class PostTag(db.Model):
    """Keys for the Post Tags"""
    __tablename__="post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    post_tag_id = db.Column(db.Integer, db.ForeignKey("tag.tag_id"), primary_key=True)
    

class Tag(db.Model):
    """Tag keys and names"""
    __tablename__="tag"

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name=db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="post_tags",
        # cascade="all,delete",
        backref="tag",
    )



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)