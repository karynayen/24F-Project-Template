#################################################
# reviews blueprint of endpoints
#################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#-------------------------------------------------
# Create a new blueprint object which is a collection
# of routes.
reviews = Blueprint('reviews', __name__)

#-------------------------------------------------
# Get all reviews from the system
@reviews.route('/reviews', methods=['GET'])
def get_reviews():
    query = '''
        SELECT reviewID,
               positionID,
               companyID,
               authorID,
               title,
               rating,
               recommend,
               pay_type,
               pay,
               job_type,
               date_time,
               verified,
               text
        FROM reviews
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query)

    theData = cursor.fetchall()

    response = make_response(jsonify(theData))

    response.status_code = 200

    return response
#---------------------------------------------------
# Add a new review to the system
@reviews.route('/review', methods=['POST'])
def add_new_review():

    the_data = request.json
    current_app.logger.info(the_data)

    positionID = the_data['review_positionID']
    companyID = the_data['review_companyID']
    authorID = the_data['review_authorID']
    title = the_data['review_title']
    rating = the_data['review_rating']
    recommend = the_data['review_recommend']
    pay_type = the_data['review_pay_type']
    pay = the_data['review_pay']
    job_type = the_data['review_job_type']
    date_time = the_data['review_date_time']
    verified = the_data['review_verified']
    text = the_data['review_text']

    query = f'''
        INSERT INTO reviews (position_ID,
                             companyID,
                             authorID,
                             title,
                             rating,
                             recommend,
                             pay_type,
                             pay,
                             job_type,
                             date_time,
                             verified,
                             text)
        VALUES ('{str(positionID)}', '{str(companyID)}', '{str(authorID)}',
                '{title}', '{str(rating)}', '{str(recommend)}',
                '{pay_type}', '{str(pay)}', '{job_type}', '{date_time}',
                '{str(verified)}', '{text}')
    '''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added review")
    response.status_code = 200
    return response

#-----------------------------------------------------------------
# Update a review in the system
@reviews.route('/reviews', methods=['PUT'])
def update_review():
    current_app.logger.info('PUT /reviews route')
    rev_info = request.json
    rev_id = rev_info['reviewID']
    rating = rev_info['rating']
    verified = rev_info['verified']
    text = rev_info['text']

    query = 'UPDATE reviews SET rating = %s, verified = %s, text = %s where reviewID = %s'
    data = (rating, verified, text, rev_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'review updated!'

#-------------------------------------------------------------------
# Delete a review from the system
@reviews.route('/review', methods=['DELETE'])
def delete_review():
    current_app.logger.info('DELETE /review route')
    rev_info = request.json
    rev_id = rev_info['reviewID']

    query = 'DELETE FROM reviews WHERE reviewID = %s'
    data = (rev_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'review removed!'

#--------------------------------------------------------------------
# Get a specific review based on reviewID from the system
@reviews.route('/reviews/<reviewID>', methods=['GET'])
def get_review(reviewID):
    query = f'''
        SELECT * FROM reviews WHERE reviewID = {reviewID}
    '''

    current_app.logger.info(f'GET /reviews/{reviewID} query={query}')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID} Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#--------------------------------------------------------------------
# Update a specific review based on reviewID from the system
@reviews.route('/reviews/<reviewID>', methods=['PUT'])
def update_specific_review(reviewID):
    current_app.logger.info('PUT /reviews/<reviewID> route')
    rev_info = request.json
    rating = rev_info['rating']
    verified = rev_info['verified']
    text = rev_info['text']

    query = 'UPDATE reviews SET rating = %s, verified = %s, text = %s where reviewID = %s'
    data = (rating, verified, text, reviewID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'review updated!'

#----------------------------------------------------------------------
# Get all questions associated with a specific review
@reviews.route('/reviews/<reviewID>/questions', methods=['GET'])
def get_review_questions(reviewID):
    current_app.logger.info('GET /reviews/<reviewID>/questions route')
    query = f'''
        SELECT * FROM questions WHERE reviewID = {reviewID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID}/questions Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#----------------------------------------------------------------------
# Add a new question to a specific review
@reviews.route('/reviews/<reviewID>/questions', methods=['POST'])
def add_review_question(reviewID):
    the_data = request.json
    current_app.logger.info(the_data)

    postID = the_data[reviewID]
    author = the_data['questions_author']
    text = the_data['questions_text']

    query = f'''
        INSERT INTO questions (postId,
                               author,
                               text)
        VALUES ('{postID}', '{author}', '{text}')
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response('Successfully added question')
    response.status_code = 200
    return response

#-----------------------------------------------------------------
# Get all answers associated with a specific review
@reviews.route('/reviews/<reviewID/answers', methods=['GET'])
def get_review_answers(reviewID):
    current_app.logger.info('GET /reviews/<reviewID>/answers route')
    query = f'''
        SELECT * FROM answers WHERE reviewID = {reviewID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID}/answers Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#-------------------------------------------------------------------
# Add a new answer to a specific review
@reviews.route('/reviews/<reviewID>/answers', methods=['POST'])
def add_review_answer(reviewID):
    the_data = request.json
    current_app.logger.info(the_data)

    postID = the_data[reviewID]
    questionID = the_data['answers_questionId']
    author = the_data['answers_author']
    text = the_data['answers_text']

    query = f'''
        INSERT INTO questions (postId,
                               questionId
                               author,
                               text)
        VALUES ('{postID}', '{questionID}', '{author}', '{text}')
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response('Successfully added answer')
    response.status_code = 200
    return response