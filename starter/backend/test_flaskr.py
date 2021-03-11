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

        self.new_question = {
            'question': 'Who won the 2008 Champions League Final?',
            'answer': 'Manchester United',
            'category': 6,
            'difficulty': 2 
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

    '''TEST: DELETE '''
    def test_delete_question(self):
        res = self.client().delete('/questions/17')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 17)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    
    def test_422_question_does_not_exist(self):
        res = self.client().delete('questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
    
    '''TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab. ''' 
  
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')
    

    def test_search_query(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'Tom Hanks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']), 1)

      


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()