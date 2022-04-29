import unittest
from server import app
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, example_data, db
import crud
from jinja2 import StrictUndefined
from model import db, User, Appointment, connect_to_db
import os


class MelonScheduler(unittest.TestCase):
    """Tests for Melon Tasting Scheduler app """

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] =  True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Log In", result.data)
        

class MelonSchedulerDataBase(unittest.TestCase):
    """Tests for Melon Tasting Scheduler database"""

    def setUp(self):
        """ To do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///mtr_data")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """ Test the sign up form"""
        
        result = self.client.post("/login", data={'username': 'beatriz'},
                                            follow_redirects=True)
        self.assertIn(b"Schedule an Appointment", result.data)

if __name__ == "__main__":
    unittest.main()