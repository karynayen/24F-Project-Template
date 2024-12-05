from flask import Flask

from backend.db_connection import db
from backend.companies.companies_routes import companies
from backend.questions.questions_routes import questions
from backend.answers.answers_routes import answers
from backend.reviews.reviews_routes import reviews
from backend.positions.positions_routes import positions
from backend.colleges.college_routes import colleges
from backend.industries.industries_routes import industries
from backend.reviewers.reviewers_routes import reviewers

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = "glasshusky" # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(reviews,     url_prefix='/r')
    app.register_blueprint(companies,   url_prefix='/co')
    app.register_blueprint(questions,   url_prefix='/q')
    app.register_blueprint(answers,     url_prefix='/a')
    app.register_blueprint(positions,   url_prefix='/po')
    app.register_blueprint(colleges,    url_prefix='/col')
    app.register_blueprint(industries,   url_prefix='/i')
    app.register_blueprint(reviewers,   url_prefix='/rver')

    # Don't forget to return the app object
    return app
