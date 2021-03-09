import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password123','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_category = {
            'type': 'Technology'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    TEST 1 FOR GET CATEGORIES'''
    
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))
    
   # def test_404_sent_requesting_nothing_to_retrieve(self):
       # res = self.client().get('/categories', json={'categories': None})
        #data = json.loads(res.data)

        #self.assertEqual(res.status_code, 404)
        #self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], 'Not Found')
    'Test 2 for Questions'
    def test_retrieve_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
    
    def test_404_sent_reuqest_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    '''TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. '''
    
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()