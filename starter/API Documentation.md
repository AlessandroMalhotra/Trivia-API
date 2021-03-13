## Trivia API Documentation


### Introduction
The API is used to configure and play the udacity trivia game.


### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
API Keys /Authentication: The Trivia API doesn't use HTTP Header Authentication.
Version: The current version of the API is v0.1 ;)


### Errors
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
Response codes & types:

400: Bad Request
404: Resource Not Found
405: Mehtod not allowed
422: Not Processable


### Resource endpoint library


#### GET /categories

Descr.: Returns a list of all available quiz categories.
Sample CURL: curl -X GET http://localhost:3000/categories

Arguments: None
Response Object: ''' { "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "success": true } '''


#### GET /questions

Descr.: Returns a list of questions, number of total questions, current category, categories including pagination suppport.
Sample CURL: curl -X GET http://localhost:3000/questions

Arguments: None

Response Object: ''' { "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "questions": [ { "answer": "Lake Victoria", "category": 3, "difficulty": 2, "id": 13, "question": "What is the largest lake in Africa?" }, { "answer": "The Palace of Versailles", "category": 3, "difficulty": 3, "id": 14, "question": "In which royal palace would you find the Hall of Mirrors?" } ], "success": true, "total_questions": 22 } '''


#### GET /categories/int:id/questions

Descr.: Get a list of questions by category to be able to play the game only with questions of one category
Sample CURL: curl -X GET http://localhost:3000//categories/int:category_id/questions

Arguments: ''' Existing available Categories are: id | type
----+--------------- 1 | Science 2 | Art 3 | Geography 4 | History 5 | Entertainment 6 | Sports
'''

Response Object: ''' { "currentCategory": "Science", "questions": [ { "answer": "The Liver", "category": 1, "difficulty": 4, "id": 20, "question": "What is the heaviest organ in the human body?" }, { "answer": "Alexander Fleming", "category": 1, "difficulty": 3, "id": 21, "question": "Who discovered penicillin?" }, { "answer": "Blood", "category": 1, "difficulty": 4, "id": 22, "question": "Hematology is a branch of medicine involving the study of what?" } ], "success": true, "totalQuestions": 22 } '''


#### DELETE /questions/int:question_id

Descr.: Deletes a selected question by ID
Sample CURL: curl -X DELETE http://localhost:3000/questions/int:question_id

Arguments: int:question_id
Response Object: ''' { "success": true } '''
// QUESTION: WHY doesn't that CURL not work?


#### POST /questions

Descr.: Adds a question to the quiz
Sample CURL: curl -X POST http://localhost:3000/questions -H "Content-Type: application/json" -d '{question: "Who am I", answer: "Uwe", difficulty: 1, category: "6"}'

Arguments: ''' {"question":"Where", "answer":"here", "category":"5","difficulty":"2"} '''
Response Object: ''' { "success": true } '''


#### POST /questions/search

Descr.: Searches for questions. When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page of the questions list in the "List" tab.
Sample CURL: curl -X POST http://localhost:3000/search_questions -H "Content-Type: application/json" -d '{searchTerm: "Boxer"}'

Arguments: ''' {searchTerm: "Boxer"} '''
Response Object: ''' { "success": true } '''


#### POST /quizzes

Descr.: Creates a question set for a quiz based on a given category and already asked quesiosn
Sample CURL: curl -X POST http://localhost:3000/quizzes -H "Content-Type: application/json" -d '{previous_questions: [], quiz_category: {type: "Sports", id: "25"}}'

Arguments: ''' {previous_questions: [], quiz_category: {type: "Art", id: "2"}} '''

Response Object: ''' { "question": { "answer": "Manchester United", "category": 6, "difficulty": 3, "id": 24, "question": "Who won the 2008 Champions League Final?" }, "success": true } '''