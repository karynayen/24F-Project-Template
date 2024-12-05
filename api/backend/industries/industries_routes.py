########################################################
# industries blueprint of endpoints
########################################################

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
industries = Blueprint('industries', __name__)

#------------------------------------------------------------
# Get all industries and their information
@industries.route('/industries', methods=['GET'])
def get_industries(): 
    query = 'SELECT * FROM industry'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# This is a POST route to add a new industry.
# Remember, we are using POST routes to create new entries in the database. 
@industries.route('/industries', methods=['POST'])
def add_new_industry():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['name']
    
    query = '''
        INSERT INTO `industry` (name)
        VALUES (%s)
    '''

    current_app.logger.info(query, name)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, name)
    db.get_db().commit()
    
    response = make_response("Successfully added industry")
    response.status_code = 200
    return response

# update an industry
@industries.route('/industries', methods=['PUT'])
def update_industry():
    current_app.logger.info('PUT /industries/<industryID> route')
    industry_info = request.json
    industryID = industry_info['industryID']
    name = industry_info['name']

    query = 'UPDATE industry SET name = %s where industryID = %s'
    data = (name, industryID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'industry updated!'

# delete an industry
@industries.route('/industries/<int:industryID>', methods=['DELETE'])
def delete_position(industryID):
    query = 'DELETE FROM industry WHERE industryID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (industryID))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Industry deleted successfully"}))
    response.status_code = 200
    return response

# Get all industry IDs
@industries.route('/industryIDs', methods = ['GET'])
def get_all_industryIDs():
    query = '''
        SELECT DISTINCT industryID AS label, industryID as value
        FROM industry
        ORDER BY industryID
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response