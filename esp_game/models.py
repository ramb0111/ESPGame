from datetime import datetime
from enum import Enum

from esp_game import db
from esp_game import helper as hl


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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
        self.created_on = datetime.now()
        self.updated_on = datetime.now()

    def is_active(self):
        """Gives user status"""
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True as the user is by default authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class PrimaryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, url):
        self.url = url
        self.created_on = datetime.now()


class SecondaryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, url):
        self.url = url
        self.created_on = datetime.now()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player1_answer_count = db.Column(db.Integer, nullable=False, default=0)
    player2_answer_count = db.Column(db.Integer, nullable=False, default=0)
    primary_images_id = db.Column(db.String(1000))
    status = db.Column(db.Enum('init', 'success', 'fail', name='task_enum'), nullable=False,
                       default='init')
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, player_id):
        self.created_on = datetime.now()
        self.player1_id = player_id
        self.primary_images_id = hl.get_random_primary_images()


class PrimarySecondaryMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_id = db.Column(db.Integer, db.ForeignKey('primary_image.id'))
    secondary_id = db.Column(db.Integer, db.ForeignKey('secondary_image.id'))
    related_votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, primary_id, secondary_id):
        self.primary_id = primary_id
        self.secondary_id = secondary_id


class TaskRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    primary_id = db.Column(db.Integer, db.ForeignKey('primary_image.id'),nullable=False)
    related = db.Column(db.String(1000), nullable=False)

    def __init__(self, task_id, player_id, primary_id, related):
        self.player_id = player_id
        self.task_id = task_id
        self.primary_id = primary_id
        self.related = related


def init_db():
    db.create_all()

#
# if __name__ == '__main__':
#     db.session.commit()