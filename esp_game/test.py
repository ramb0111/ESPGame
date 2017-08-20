import os
import pytest

from flask_login import current_user
from flask_wtf.csrf import generate_csrf
import unittest

from app import app
from esp_game import db
import constants as cons
import helper as hl
from models import *

"""
For testing , create a temporary database. Lets say : game_temp
"""


class FlaskrTestCase(unittest.TestCase):
    """
    Flask Test Class for testing the APIs
    """

    def setUp(self):
        """
        Function to create tables in the temporary database
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tester:password@localhost:5432/game_temp"
        app.testing = True
        app.config['WTF_CSRF_ENABLED']=False
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """
        Function to drop the tables in the temporary database
        """
        with app.app_context():
            db.drop_all()

    def login(self, email, password):
        """
        Function to login the current user
        """
        return self.app.get ('/login', data=dict(
            email=email,
            password=password,
            csrf_token=generate_csrf()
        ), follow_redirects=True)

    def logout(self):
        """
        Function to logout the current user
        """
        return self.app.get('/logout', follow_redirects=True)

    def test_get_random_primary_images(self):
        """
        Test function to check iof all the ids are in range from 1 to 15
        :return:
        """
        ids_list = get_random_primary_images().split(' ')
        ids_list = map(int, ids_list)
        for id in ids_list:
            if not 1 <= id <= cons.PRIMARY_IMAGES_COUNT:
                assert False
        assert True



if __name__ == '__main__':
    unittest.main()
