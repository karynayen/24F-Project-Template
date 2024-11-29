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
    query = '''
        SELECT major, name, num_co-ops, year, num_posts, bio 
        FROM reviewer r
    '''
    
    # get a cursor object from the database~ cursor is like 2d grid that you can iterate over with your code
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # fetch all the data from the cursor
    # The cursor will return the data as a 
    # Python Dictionary
    theData = cursor.fetchall()

    # Create a HTTP Response object and add results of the query to it
    # after "jasonify"-ing it.
    response = make_response(jsonify(theData))
    # set the proper HTTP Status code of 200 (meaning all good)
    response.status_code = 200
    # send the response back to the client
    return response


# ------------------------------------------------------------
# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@reviewers.route('/reviewers/<reviewerID>', methods=['PUT'])
def add_new_reviewer():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    major = the_data['major']
    name = the_data['reviewer_name']
    num_coops = the_data['num_coops']
    year = the_data['year']
    bio = the_data['bio']
    active = the_data['active']
    
    query = f'''
        INSERT INTO reviewer (major, name, num_co-ops, year, num_posts, bio, active)
        VALUES ('{major}', '{name}', '{num_coops}', '{year}', '{bio}', '{active}',)
    '''
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
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added product")
    response.status_code = 200
    return response


