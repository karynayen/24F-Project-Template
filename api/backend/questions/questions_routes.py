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
@questions.route('/questions', methods=['PUT'])
def edit_question(): 
    query = f'''
        UPDATE {table_name} 
        SET {column} = {new_value}
        WHERE {condition};
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------

