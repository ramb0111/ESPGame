import datetime
from enum import Enum

from esp_game import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    points = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.created_on = datetime.datetime()
        self.updated_on = datetime.datetime()


class PrimaryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, url):
        self.url = url
        self.created_on = datetime.datetime()


class SecondaryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, url):
        self.url = url
        self.created_on = datetime.datetime()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player1_answer_count = db.Column(db.Integer, nullable=False, default=0)
    player2_answer_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum(Enum('init', 'success', 'fail')), nullable=False, default=True)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, player_id):
        self.status = 'init'
        self.created_on = datetime.datetime()
        self.player1_id = player_id


class PrimarySecondaryMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_id = db.Column(db.Integer, db.ForeignKey('primary_image.id'))
    secondary_id = db.Column(db.Integer, db.ForeignKey('secondary_image.id'))
    related_votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, primary_id, secondary_id, related_votes):
        self.primary_id = primary_id
        self.secondary_id = secondary_id
        self.related_votes = related_votes


class TaskRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prim_sec_map_id = db.Column(db.Integer, db.ForeignKey('primary_secondary_mapping.id'),
                                nullable=False)
    related = db.Column(db.Boolean, nullable=False)

    def __init__(self, task_id, player_id, prim_sec_map_id, related):
        self.player_id = player_id
        self.task_id = task_id
        self.prim_sec_map_id = prim_sec_map_id
        self.related = related


def init_db():
    db.create_all()
