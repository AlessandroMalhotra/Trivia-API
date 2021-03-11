import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

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
    cat = Category.query.all()
    categories = {}
    for category in cat:
      categories[category.id] = category.type

    if len(cat) == 0:
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
  

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    req = request.get_json()
    search_term = req.get('searchTerm', '')
    
    try:
      results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      
      if not results:
        abort(422)
      
      searched_questions = paginate_questions(request, results)
      
      return jsonify({
        'success': True,
        'questions': searched_questions,
        'total_questions': len(results)
      })
    
    except:
      print(sys.exc_info())
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  
  create a app.route with questions/category_id as route with methods post
  then define a function called question by category
  Inside the function do req = request.getjson() then a questions_id = req.get('category', '')
  Inside try : Then we query the question database with the above varibale and get all questions with that category id,
  then paginate and return a jsonify object end try
  Inside except: throw error 404 or 422
  
  (Then query the category database to get the category which match that id) maybe
   
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

    