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
  
  # DONE
  ''' @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs '''
  
  CORS(app, resources={r"/api/*":{"origins":"*"}})
 
  
  # DONE 
  ''' @TODO: Use the after_request decorator to set Access-Control-Allow '''
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response


  # DONE
  ''' @TODO: Create an endpoint to handle GET requests for all available categories. '''
  
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
  

  # DONE
  ''' @TODO: Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  This endpoint should return a list of questions, number of total questions, current category, categories. '''
 
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
  
 
  # DONE
  ''' @TODO: Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed. This removal will persist in the database and when you refresh the page. '''
  
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

 
   # DONE
  ''' @TODO: Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end 
  of the last page of the questions list in the "List" tab. '''

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
  

  # DONE
  ''' @TODO: Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term 
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. Try using the word "title" to start.'''

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

  
  # DONE
  ''' @TODO: Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. '''

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

  
   # DONE
  ''' @TODO: Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters 
  and return a random questions within the given category, if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category, one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. '''

  @app.route('/quizzes', methods=['POST'])
  def create_quiz():
    req = request.get_json()
    previous_questions = req.get('previous_questions', [])
    quiz_category = req.get('quiz_category', 0)

    try:
      if quiz_category['id'] == 0:
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        questions = Question.query.filter(Question.category==quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
      
      if len(questions) == 0:
        abort(400)
        return jsonify({
          'success': True,
          'question': None
        })
      formatted_questions = random.choice(questions).format()
  
    except:
      abort(400)
    
    return jsonify({
      'success': True,
      'question': formatted_questions
    })


   # DONE
  ''' @TODO: Create error handlers for all expected errors including 404 and 422. '''

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

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
    }), 400
  
  return app