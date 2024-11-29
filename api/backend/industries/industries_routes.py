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
# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@industries.route('/industries', methods=['POST'])
def add_new_industry():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['industry_name']
    id = the_data['industryID']
    
    query = f'''
        INSERT INTO industry (name, industryID)
        VALUES ('{name}', '{id}')
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



# # ------------------------------------------------------------
# # get product information about a specific product
# # notice that the route takes <id> and then you see id
# # as a parameter to the function.  This is one way to send 
# # parameterized information into the route handler.
# @products.route('/product/<id>', methods=['GET'])
# def get_product_detail (id):

#     query = f'''SELECT id, 
#                        product_name, 
#                        description, 
#                        list_price, 
#                        category 
#                 FROM products 
#                 WHERE id = {str(id)}
#     '''
    
#     # logging the query for debugging purposes.  
#     # The output will appear in the Docker logs output
#     # This line has nothing to do with actually executing the query...
#     # It is only for debugging purposes. 
#     current_app.logger.info(f'GET /product/<id> query={query}')

#     # get the database connection, execute the query, and 
#     # fetch the results as a Python Dictionary
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     theData = cursor.fetchall()
    
#     # Another example of logging for debugging purposes.
#     # You can see if the data you're getting back is what you expect. 
#     current_app.logger.info(f'GET /product/<id> Result of query = {theData}')
    
#     response = make_response(jsonify(theData))
#     response.status_code = 200
#     return response
    
# # ------------------------------------------------------------
# # Get the top 5 most expensive products from the database
# @products.route('/mostExpensive')
# def get_most_pop_products():

#     query = '''
#         SELECT product_code, 
#                product_name, 
#                list_price, 
#                reorder_level
#         FROM products
#         ORDER BY list_price DESC
#         LIMIT 5
#     '''
    
#     # Same process as handler above
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     theData = cursor.fetchall()
 
#     response = make_response(jsonify(theData))
#     response.status_code = 200
#     return response

# # ------------------------------------------------------------
# # Route to get the 10 most expensive items from the 
# # database.

# @products.route('/tenMostExpensive', methods=['GET'])
# def get_10_most_expensive_products():
    
#     query = '''
#         SELECT product_code, 
#                product_name, 
#                list_price, 
#                reorder_level
#         FROM products
#         ORDER BY list_price DESC
#         LIMIT 10
#     '''
    
#     # Same process as above
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     theData = cursor.fetchall()
    
#     response = make_response(jsonify(theData))
#     response.status_code = 200
#     return response
    


# # ------------------------------------------------------------
# ### Get all product categories
# @products.route('/categories', methods = ['GET'])
# def get_all_categories():
#     query = '''
#         SELECT DISTINCT category AS label, category as value
#         FROM products
#         WHERE category IS NOT NULL
#         ORDER BY category
#     '''

#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     theData = cursor.fetchall()
        
#     response = make_response(jsonify(theData))
#     response.status_code = 200
#     return response

# # ------------------------------------------------------------
# ### Getting 8 items that have been ordered most frequently
# ### product name, supplier name, number of orders, ties broken by alphabetizing product name
# @products.route('/eightmostfrequent', methods = ['GET'])
# def get_8_most_frequent():
#     query = '''
#         SELECT p.product_name, s.company AS supplier_name, COUNT(od.OrderID) AS order_count
#         FROM products p
#             JOIN suppliers s ON p.SupplierID =  s.SupplierID
#             JOIN order_details od ON p.ProductID = od.ProductID
#         GROUP BY p.product_name, s.company
#         ORDER BY NumOrders DESC, p.product_name ASC
#         LIMIT 8
#         '''
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     theData = cursor.fetchall()

#     response = make_response(jsonify(theData))
#     response.status_code = 200
#     return response
# # ------------------------------------------------------------
# # This is a stubbed route to update a product in the catalog
# # The SQL query would be an UPDATE. 
# @products.route('/product', methods = ['PUT'])
# def update_product():
#     product_info = request.json
#     current_app.logger.info(product_info)

#     return "Success"