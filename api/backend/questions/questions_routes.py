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
        
        check_questionId_query = "SELECT * FROM questions WHERE questionId = %s"
        cursor.execute(check_questionId_query, (questionId,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Question not found"}), 404
        
        return jsonify({"message": "Question Updated!"}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error updating question {questionId}: {str(e)}')
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500
    