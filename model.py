from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from exts import db

users_courses = db.Table('users_courses',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
            )


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(256))

    messages = db.relationship('Message', backref='user')

    comments = db.relationship('Comment', back_populates='user', cascade='all')
    courses = db.relationship('Course', secondary=users_courses,
                                    back_populates='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(30))
    teacher = db.Column(db.String(30))
    classroom = db.Column(db.String(30))
    description = db.Column(db.Text)

    # comments = db.relationship('Comment', back_populates='course', cascade='all')
    users = db.relationship('User', secondary=users_courses, back_populates='courses')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   # course = db.relationship('Course', back_populates='comments')
    user = db.relationship('User', back_populates='comments')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    love_num = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment')



