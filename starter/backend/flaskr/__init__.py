import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, results):
   page = request.args.get('page', 1, type=int)
   start = (page - 1) * QUESTIONS_PER_PAGE
   end = start + QUESTIONS_PER_PAGE

   questions = [question.format() for question in results]
   current_question = questions[start:end]

   return current_question


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*":{"origins":"*"}})
 

  @app.after_request
  def after_request(response):
    response.headers.add('Access-control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response

  
  @app.route('/categories')
  def show_all_categories():
    results = Category.query.order_by(Category.id).all()
    categories = [category.format() for category in results]

    if len(results) == 0:
      abort(400)
    
    return jsonify({
      'success': True,
      'categories': categories
    })
  

  @app.route('/questions', methods=['GET'])
  def show_questions():
    results = Question.query.order_by(Question.id).all()
    questions = paginate_questions(request, results)
    
    get_categories = Category.query.all()
    categories = [category.format() for category in get_categories]

   
    if len(questions) == 0:
      abort(404)
   
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(results),
      'categories': categories
    })
  
 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      
      question.delete()
      
      results = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, results)
      
      return jsonify({
      'success': True,
      'deleted': question_id,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
    })

    except:
      abort(422)
    
    finally:
      db.session.close()

 
  @app.route('/questions', methods=['POST'])
  def create_question():
    req = request.get_json()

    question = req.get('question', None)
    answer = req.get('answer', None)
    difficulty = req.get('difficulty', None)
    category = req.get('category', None)

    try:
      new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      new_question.insert()

      results = Question.query.order_by(Question.id).all()
      questions = paginate_questions(request, results)

      return jsonify({
        'success': True,
        'created': new_question.id,
        'questions': questions,
        'total_questions': len(Question.query.all())
      })
  
    except:
      abort(405)
  
    finally:
      db.session.close()
  
  '''TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab. ''' 
  

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405
  
  return app

    