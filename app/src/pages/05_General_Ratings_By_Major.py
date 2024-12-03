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
st.header('General Ratings By Major')


# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

college_data = {} 

try: 
    college_data = requests.get('http://api:4000/col/colleges').json()

    for college in college_data:
        with st.container(border=True):
            st.write(f"##### {college['name']} Ratings:")
            college_positions = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews').json()

            answers = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews/answers').json()
            questions = requests.get('http://api:4000/col/colleges/' + str(college['collegeID']) + '/reviews/questions').json()

            answer_count = len(answers)
            question_count = len(questions)
            # st.dataframe(college_positions)
            all_ratings = []
            for position in college_positions:
                all_ratings.append(position['rating'])
            average_rating = round(np.mean(all_ratings), 2) or None

            all_dates = []
            for position in college_positions:
                all_dates.append(position['date_time'])
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
                    # fig = px.histogram(all_ratings, x=all_ratings, title='Ratings Distribution')
                    # st.plotly_chart(fig)
                    # TODO add a range of dates
                    fig = px.histogram(all_ratings, x=all_dates, title='Ratings Distribution Over Time')
                    st.plotly_chart(fig, key=str(college['collegeID']))

except:
    st.write("Error rendering page")




