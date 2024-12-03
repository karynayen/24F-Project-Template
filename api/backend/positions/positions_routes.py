from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

positions = Blueprint('positions', __name__)

# Get all positions
@positions.route('/positions', methods=['GET'])
def get_positions():
    query = 'SELECT * FROM position'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    positions_data = cursor.fetchall()
    response = make_response(jsonify(positions_data))
    response.status_code = 200
    return response

# Get a specific position by ID
@positions.route('/positions/<int:positionID>', methods=['GET'])
def get_position(positionID):
    query = 'SELECT * FROM position WHERE positionID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (positionID,))
    position_data = cursor.fetchone()
    if position_data:
        response = make_response(jsonify(position_data))
        response.status_code = 200
    else:
        response = make_response(jsonify({"error": "Position not found"}))
        response.status_code = 404
    return response

# Add a new position
@positions.route('/positions', methods=['POST'])
def add_position():
    data = request.json
    companyID = data['companyID']
    name = data['name']
    description = data.get('description', '')
    remote = data['remote']
    
    query = '''
        INSERT INTO position (companyID, name, description, remote)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (companyID, name, description, remote))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Position added successfully"}))
    response.status_code = 201
    return response

# Update an existing position
@positions.route('/positions/<int:positionID>', methods=['PUT'])
def update_position(positionID):
    data = request.json
    name = data['name']
    description = data.get('description', '')
    remote = data['remote']
    
    query = '''
        UPDATE position
        SET name = %s, description = %s, remote = %s
        WHERE positionID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, description, remote, positionID))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Position updated successfully"}))
    response.status_code = 200
    return response

# Delete a position
@positions.route('/positions/<int:positionID>', methods=['DELETE'])
def delete_position(positionID):
    query = 'DELETE FROM position WHERE positionID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (positionID,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Position deleted successfully"}))
    response.status_code = 200
    return response