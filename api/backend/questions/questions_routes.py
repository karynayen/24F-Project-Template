########################################################
# questions blueprint of endpoints
#######################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
questions = Blueprint('questions', __name__)

#------------------------------------------------------------
# Get all questions
@questions.route('/questions', methods=['GET'])
def get_answers():
    query = 'SELECT * FROM questions'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Edit a posted questions
@questions.route('/questions/<questionId>', methods=['PUT'])
def edit_question(questionId):
    try:
        current_app.logger.info(f'PUT /questions/{questionId} route')
        question_info = request.json
        text = question_info['text']
        
        query = '''
            UPDATE questions
            SET text = %s
            WHERE questionId = %s
        '''
        
        data = (text, questionId)
        cursor = db.get_db().cursor()
        r = cursor.execute(query, data)
        db.get_db().commit()
        
        current_app.logger.info(f'Question {questionId} successfully updated!')
        
        check_questionId_query = 'SELECT * FROM questions WHERE questionId = %s'
        cursor.execute(check_questionId_query, (questionId,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Question not found'}), 404
        
        return jsonify({'message': 'Question Updated!'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error updating question {questionId}: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    
#------------------------------------------------------------
# Delete questions
@questions.route('/questions/<questionId>', methods=['DELETE'])
def delete_quesitons(questionId):
    try:
        current_app.logger.info(f'DELETE /questions/{questionId} route')
        question_info = request.json
        
        check_questionId_query = '''
            SELECT * 
            FROM questions
            WHERE questionId = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(check_questionId_query, (questionId,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Question not found'}), 404
        
        
        query = '''
            DELETE FROM questions
            WHERE questionId = %s
        '''
        
        cursor.execute(query, (questionId,))
        db.get_db().commit()
        current_app.logger.info(f'Question {questionId} successfully deleted!')
        return jsonify({'message': 'Question Deleted!'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error deleting question {questionId}: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    

#-------------------------------------------------------------
# Get all question Ids
@questions.route('/questionIds', methods = ['GET'])
def get_all_questionIds():
    query = '''
        SELECT DISTINCT questionId AS label, questionId as value
        FROM questions
        ORDER BY questionId
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get questions associated with a post
@questions.route('/questions/<int:postId>', methods=['GET'])
def get_questions(postId):
    try:
        current_app.logger.info(f'GET /questions/{postId} route')
        
        get_questions_query = '''
            SELECT text 
            FROM questions
            WHERE postId = %s
        '''
        
        db.get_db().commit()
        with db.get_db().cursor() as cursor:
            cursor.execute(get_questions_query, (postId,))
            questions = cursor.fetchall()
        
        if not questions:
            return jsonify({'message': 'No questions found for this post'}), 404
     
        
        return jsonify({f'Question': questions}), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting questions for postId {postId}: {str(e)}')
        return jsonify({'error': 'An internal server error occurred'}), 500
