########################################################
# answers blueprint of endpoints
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
answers = Blueprint('answers', __name__)

#------------------------------------------------------------
# Get all answers
@answers.route('/answers', methods=['GET'])
def get_answers():
    query = 'SELECT * FROM answers'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Edit a posted answers
@answers.route('/answers/<answerId>', methods=['PUT'])
def edit_answer(answerId):
    try:
        current_app.logger.info(f'PUT /answers/{answerId} route')
        answer_info = request.json
        text = answer_info['text']
        
        query = '''
            UPDATE answers
            SET text = %s
            WHERE answerId = %s
        '''
        
        data = (text, answerId)
        cursor = db.get_db().cursor()
        r = cursor.execute(query, data)
        db.get_db().commit()
        
        current_app.logger.info(f'answer {answerId} successfully updated!')
        
        check_answerId_query = 'SELECT * FROM answers WHERE answerId = %s'
        cursor.execute(check_answerId_query, (answerId,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'answer not found'}), 404
        
        return jsonify({'message': 'answer Updated!'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error updating answer {answerId}: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    
#------------------------------------------------------------
# Delete answers
@answers.route('/answers/<answerId>', methods=['DELETE'])
def delete_quesitons(answerId):
    try:
        current_app.logger.info(f'DELETE /answers/{answerId}' 'route')
        answer_info = request.json
        
        check_answerId_query = '''
            SELECT * 
            FROM answers
            WHERE answerId = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(check_answerId_query, (answerId,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'answer not found'}), 404
        
        
        query = '''
            DELETE FROM answers
            WHERE answerId = %s
        '''
        
        cursor.execute(query, (answerId,))
        db.get_db().commit()
        current_app.logger.info(f'answer {answerId} successfully deleted!')
        return jsonify({'message': 'answer Deleted!'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error deleting answer {answerId}: {str(e)}')
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    
#-------------------------------------------------------------
# Get all answer IDs
@answers.route('/answerIds', methods = ['GET'])
def get_all_answerIds():
    query = '''
        SELECT DISTINCT answerId AS label, answerId as value
        FROM answers
        ORDER BY answerId
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response