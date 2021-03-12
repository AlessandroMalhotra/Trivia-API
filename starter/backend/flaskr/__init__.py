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

  
  @app.route('/categories', methods=['GET'])
  def show_all_categories():
    cat = Category.query.all()
    categories = {}
    for category in cat:
      categories[category.id] = category.type

    if cat is None:
      abort(404)
    
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

    question = req.get('question')
    answer = req.get('answer')
    difficulty = req.get('difficulty')
    category = req.get('category')

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
      abort(422)


  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def questions_based_on_category(id):
      category_id = int(id) + 1
      results = Question.query.filter(Question.category == category_id).all()

      if not results:
        abort(404)
      
      else:
        questions_by_category = paginate_questions(request, results)
        return jsonify({
          'success': True,
          'questions': questions_by_category,
          'total_questions': len(results),
          'current_category': category_id
          })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  @app.route for questions/quiz for a post method, then define a function called quiz
  inside req = request.get_json() then category and one for previous question with[] as alternative if no previous question provided, assing to
  variable = req.get()
  Inside Try - query the question database so that we got all the questions in the database, then we want to do a if,
  to say if category then get all question sin that category if they select all then just get all questions. 
  We want random for both and (maybe paginated). 
  Then we want to for each question answered pass them to a list of previous questions and make sure random question
  is not in previous question list, if so we can return jsonify of questions 


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