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
def edit_question(): 
    current_app.logger.info('PUT/questions/<questionId> route')
    question_info = request.json
    questionId = question_info['questionId']
    text = question_info[text]
    
    
    query = '''
        UPDATE question
        SET text = %s
        WHERE questionId = %s;
    '''
    data = {questionId, text}
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    return 'Question Updated!'

#------------------------------------------------------------

