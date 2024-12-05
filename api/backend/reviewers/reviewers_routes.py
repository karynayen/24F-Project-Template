########################################################
# reviewers blueprint of endpoints
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
reviewers = Blueprint('reviewers', __name__)

#------------------------------------------------------------
# Get all the reviewers from the database, package them up,
# and return them to the client
@reviewers.route('/reviewers', methods=['GET'])
def get_reviewers(): 
    query = 'SELECT * FROM reviewer'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------
# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@reviewers.route('/reviewers', methods=['POST'])
def add_new_reviewer():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    major = the_data['major']
    name = the_data['name']
    num_coops = the_data['num_coops']
    year = the_data['year']
    bio = the_data['bio']
    active = the_data['active']
    
    query = '''
    INSERT INTO reviewer (major, `name`, `num_co-ops`, `year`, bio, active) 
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    data = (major, name, num_coops, year, bio, active)
    

    # TODO: Make sure the version of the query above works properly
    # Constructing the query
    # query = 'insert into products (product_name, description, category, list_price) values ("'
    # query += name + '", "'
    # query += description + '", "'
    # query += category + '", '
    # query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    response = make_response("Successfully added reviewer")
    response.status_code = 200
    # return response
    return response

@reviewers.route('/reviewers', methods=['PUT'])
def update_reviewer():
    current_app.logger.info('PUT /reviewers/<reviewerID> route')
    reviewer_info = request.json
    reviewerID = reviewer_info['reviewerID']
    major = reviewer_info['major']
    name = reviewer_info['name']
    num_coops = reviewer_info['num_coops']
    year = reviewer_info['year']
    bio = reviewer_info['bio']
    active = reviewer_info['active']

    query = 'UPDATE reviewer SET major = %s, `name` = %s, `num_co-ops`  = %s, `year`  = %s, bio  = %s, active  = %s where reviewerID = %s'
    data = (major, name, num_coops, year, bio, active, reviewerID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'reviewer updated!'

# Delete a reviewer
@reviewers.route('/reviewers/<int:reviewerID>', methods=['DELETE'])
def delete_reviewer(reviewerID):
    query = 'DELETE FROM reviewer WHERE reviewerID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (reviewerID))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Reviewer deleted successfully"}))
    response.status_code = 200
    return response