from app import db
import uuid
from datetime import datetime
from flask import url_for


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session = db.Column(db.String)
    vk = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    name = db.Column(db.String, unique=True)
    text = db.Column(db.Text)
    discord = db.Column(db.String)
    vk = db.Column(db.String)
    telegram = db.Column(db.String)
    link = db.Column(db.String, default=str(uuid.uuid4()), unique=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Team {}>'.format(self.body)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    count_event = db.Column(db.Integer, default=0)
    count_train = db.Column(db.Integer, default=0)
    name = db.Column(db.String)
    position = db.Column(db.String, default='Player')

    def __repr__(self):
        return '<Member {}>'.format(self.body)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    text = db.Column(db.Text)
    cancel = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_event = db.Column(db.DateTime, index=True)
    type_event = db.Column(db.String)

    def __repr__(self):
        return '<Event {}>'.format(self.body)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String)

    def __repr__(self):
        return '<Comment {}>'.format(self.body)


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    status = db.Column(db.Boolean, default=False)
    user_name = db.Column(db.String)

    def __repr__(self):
        return '<Movement {}>'.format(self.body)