from datetime import datetime
import logging

import requests
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('General Ratings By College')


# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

college_data = {} 

try: 
    college_data = requests.get('http://api:4000/col/colleges').json()

    for college in college_data:
        with st.container(border=True):
            st.write(f"##### {college['name']} Ratings:")

            # Api calls to get the reviews, questions, and answers for a specific college
            college_positions = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews').json()
            answers = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews/answers').json()
            questions = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews/questions').json()

            answer_count = len(answers)
            question_count = len(questions)

            all_ratings = list(map(lambda position: position['rating'], college_positions))
            average_rating = round(np.mean(all_ratings), 2) or None

            all_dates = list(map(lambda position: position['date_time'], college_positions))

            # Group the ratings by semester
            semester_buckets = {}
            for date, rating in zip(all_dates, all_ratings):
                datem = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
                year = datem.year
                month = datem.month
                if month >= 8 and month <= 12:
                    semester = 'Fall ' + str(year)
                elif month >= 1 and month <= 4:
                    semester = 'Spring ' + str(year)
                else:
                    semester = 'Summer ' + str(year)
                if semester in semester_buckets:
                    semester_buckets[semester].append(rating)
                else:
                    semester_buckets[semester] = [rating]

            semester_total_ratings = {}
            for semester, ratings in semester_buckets.items():
                semester_total_ratings[semester] = (len(ratings), round(np.mean(ratings), 2))
            
            # all sememester sorted in ascending order by year and then Spring, Summer, Fall 
            sorted_semesters = sorted(
                semester_total_ratings.keys(),
                key=lambda x: (int(x.split(' ')[1]), 0 if x.split(' ')[0] == 'Spring' else 1 if x.split(' ')[0] == 'Summer' else 2))

            sorted_ratings_count = []
            sorted_ratings_avg = []
            for semester in sorted_semesters:
                sorted_ratings_count.append(semester_total_ratings[semester][0])
                sorted_ratings_avg.append(semester_total_ratings[semester][1])
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                with st.container(border=True):
                    st.write('#### Average Rating:')
                    st.write(f'### {average_rating}')
                    st.write('Total Reviews:', str(len(all_ratings)))
                    st.write('Total Questions:', str(question_count))
                    st.write('Total Answers:', str(answer_count))
                    
            with col2:
                with st.container(border=True):
                    chart_data = {
                        'ratings': sorted_ratings_count,
                        'average_ratings': sorted_ratings_avg,
                        'semesters': sorted_semesters
                    }
                    df = pd.DataFrame(chart_data)
                    fig = px.histogram(
                        df, 
                        x="semesters", 
                        y="ratings", 
                        title='Number of Reviews Per Semester'
                    )
                    st.plotly_chart(fig, key=str(college['collegeID']))
except:
    st.write("Error rendering page")




