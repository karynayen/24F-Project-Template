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
# Get all companies from the system
@industries.route('/industries', methods=['GET'])
def get_industries(): 
    query = 'SELECT * FROM industry'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all the products from the database, package them up,
# and return them to the client
@industries.route('/industries/<industryID>/companies', methods=['GET'])
def get_industry(industryID):
    query = f'''
        SELECT  i.name AS industry_name,
                c.name AS company_name,
                c.size AS company_size,
                AVG(r.rating) AS overall_rating,
                COUNT(r.rating) AS num_ratings,
                COUNT(r.reviewID) AS num_reviews,
                col.name AS college_name
        FROM company c
            JOIN companyIndustry ci ON c.companyID = ci.companyID
            JOIN industry i ON i.industryID = ci.industryID
            JOIN reviews r ON c.companyID = r.companyID
            JOIN position p ON p.positionID = r.positionID
            JOIN positionTargetCollege ptc ON ptc.positionID = p.positionID
            JOIN college col ON col.collegeID = ptc.collegeID
        WHERE i.industryID = {int(industryID)}
        GROUP BY i.name, c.name, c.name, i.name, c.size, col.name
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
# This is a POST route to add a new industry.
# Remember, we are using POST routes to create new entries in the database. 
@industries.route('/industries', methods=['POST'])
def add_new_industry():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['industry_name']
    
    query = '''
        INSERT INTO `industry` (name)
        VALUES (%s)
    '''
    # TODO: Make sure the version of the query above works properly
    # Constructing the query
    # query = 'insert into products (product_name, description, category, list_price) values ("'
    # query += name + '", "'
    # query += description + '", "'
    # query += category + '", '
    # query += str(price) + ')'
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