from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

colleges = Blueprint('colleges', __name__)

# Get all colleges
@colleges.route('/colleges', methods=['GET'])
def get_colleges():
    query = 'SELECT * FROM college'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    colleges_data = cursor.fetchall()
    response = make_response(jsonify(colleges_data))
    response.status_code = 200
    return response

# Get a specific college by ID
@colleges.route('/colleges/<int:collegeID>', methods=['GET'])
def get_college(collegeID):
    query = 'SELECT * FROM college WHERE collegeID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (collegeID,))
    college_data = cursor.fetchone()
    if college_data:
        response = make_response(jsonify(college_data))
        response.status_code = 200
    else:
        response = make_response(jsonify({"error": "College not found"}))
        response.status_code = 404
    return response

# Get all reviews for a specific college
@colleges.route('/colleges/<int:collegeID>/reviews', methods=['GET'])
def get_college_reviews(collegeID):
    query = '''
        SELECT r.reviewID, r.text, r.rating, r.date
        FROM reviews r
        JOIN college c ON r.collegeID = c.collegeID
        WHERE c.collegeID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (collegeID,))
    reviews_data = cursor.fetchall()
    response = make_response(jsonify(reviews_data))
    response.status_code = 200
    return response

# Add a new college
@colleges.route('/colleges', methods=['POST'])
def add_college():
    data = request.json
    name = data['name']
    
    query = '''
        INSERT INTO college (name)
        VALUES (%s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (name,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "College added successfully"}))
    response.status_code = 201
    return response

# Update an existing college
@colleges.route('/colleges/<int:collegeID>', methods=['PUT'])
def update_college(collegeID):
    data = request.json
    name = data['name']
    
    query = '''
        UPDATE college
        SET name = %s
        WHERE collegeID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, collegeID))
    db.get_db().commit()
    response = make_response(jsonify({"message": "College updated successfully"}))
    response.status_code = 200
    return response

# Delete a college
@colleges.route('/colleges/<int:collegeID>', methods=['DELETE'])
def delete_college(collegeID):
    query = 'DELETE FROM college WHERE collegeID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (collegeID,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "College deleted successfully"}))
    response.status_code = 200
    return response
