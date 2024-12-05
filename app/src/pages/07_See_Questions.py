import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')

import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
import numpy as np
import plotly.express as px
import pandas as pd

logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module
SideBarLinks()

# # Set the header of the page
st.header('Search Reviews')

def get_answers(questionID):
    
    try:
        answers = pd.DataFrame(requests.get(f"http://api:4000/a/answers/{questionID}").json())
        st.write(f"Answer: {answers.at[0, 'answers']['text']}")
        # st.write(answers.iterrows())
        # st.write(type(answers))
    except:
        st.write("No answers yet!")


def get_questions(reviewID, post_num):
    questions = requests.get(f"http://api:4000/q/questions/{reviewID}").json()
    
    try:
        questions = pd.DataFrame(questions)
        with st.container(border=True):
            st.write(f"Post {post_num + 1}")
            for i in range(len(questions)):
                with st.expander(f"Question {i + 1}: {questions['Question'][i]['text']}", expanded=False):
                    with st.container(border=True):
                        # st.write(questions['Question'][i]['text'])
                        get_answers(i)
        
    except:
        with st.container(border=True):
            st.write("No questions yet!")
    


def get_reviews(company_info, j):
    companyID = company_info['companyID']
    reviews = pd.DataFrame(requests.get(f"http://api:4000/co/companies/{companyID}/reviews").json()).loc[:, ['title', 'text', 'reviewID']]
    
    
    for i in range(len(reviews)):
        reviewID = reviews['reviewID'][i]
        get_questions(reviewID, j)
    
    return(reviews)
    

companies = requests.get('http://api:4000/co/companies').json()
companies_df = pd.DataFrame(companies)
for i in range(len(companies_df)): 
    companyID = companies_df.iloc[i]['companyID']        
    reviews = requests.get(f"http://api:4000/co/companies/{companyID}/reviews").json()
    reviews = pd.DataFrame(reviews)
    
    company_info = companies_df.loc[i]
    reviews = get_reviews(company_info, i)
