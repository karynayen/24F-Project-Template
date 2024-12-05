########################################################
# companies blueprint of endpoints
#######################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
companies = Blueprint('companies', __name__)


#------------------------------------------------------------
# Get all companies and their information from the system
@companies.route('/companies', methods=['GET'])
def get_companies(): 
    query = '''
        SELECT *
        FROM company c
        JOIN companylocation cl ON c.companyID = cl.companyID
        JOIN location l ON cl.locID = l.locID
        JOIN companyIndustry ci ON c.companyID = ci.companyID
        JOIN industry i ON ci.industryID = i.industryID
        '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# get only the data from the company table
@companies.route('/companies_simple', methods=['GET'])
def get_companies_simple(): 
    query = '''
        SELECT *
        FROM company
        '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------

# Add a new company to the system
@companies.route('/companies', methods=['POST'])
def add_company(): 
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    size = the_data['size']
    
    query = f'''
        INSERT INTO company (name, size)
        VALUES ('{name}', '{size}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added company")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get company detail for company with particular companyID
@companies.route('/companies/<companyID>', methods=['GET'])
def get_company(companyID):
    query = f'''
        SELECT * FROM company WHERE companyID = {companyID}
    '''
    current_app.logger.info(f'GET /companies/{companyID} query={query}')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID} Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


#------------------------------------------------------------
# Update company info for company with particular companyID
@companies.route('/companies/<companyID>', methods=['PUT'])
def update_company(companyID): 
    current_app.logger.info('PUT /companies/<companyID> route')
    company_info = request.json
    name = company_info['name']
    size = company_info['size']

    query = 'UPDATE company SET name = %s, size = %s where companyID = %s'
    data = (name, size, companyID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'company updated!'


#------------------------------------------------------------
# Return all reviews associated with a particular company
@companies.route('/companies/<companyID>/reviews', methods=['GET'])
def get_company_reviews(companyID):
    current_app.logger.info('GET /companies/<companyID>/reviews route')
    query = f'''
        SELECT * FROM reviews WHERE companyID = {companyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID}/reviews Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete a company from the system
# Note due to foreign key constraints, you can only delete a company if it has no other references
@companies.route('/companies/<companyID>', methods=['DELETE'])
def delete_company(companyID):
    current_app.logger.info('DELETE /companies/<companyID> route')
    query = f'''
        DELETE FROM company WHERE companyID = {companyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'company deleted!'

#-------------------------------------------------------------
# Get all company IDs
@companies.route('/companyIDs', methods = ['GET'])
def get_all_companyIDs():
    query = '''
        SELECT DISTINCT companyID AS label, companyID as value
        FROM company
        ORDER BY companyID
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
