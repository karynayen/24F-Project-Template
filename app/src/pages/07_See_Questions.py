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
# def create_review_card(company, reviews):
    
    
    # # Make review card
    # with st.container(border=True):
    #     for review in reviews.iterrows():
            
    #         with st.container(border=True):
    #             st.write(f"### {company['name']} Review:")
    #             st.write(f"**{review[1]['name']}** - {review[1]['title']}")
    #             st.write(review[1]['text'])
    #             st.write(f"Pay type: {review[1]['pay_type']}.")
    #             st.write(f"Pay rate: {review[1]['pay']}")
    #             st.write(f"Rating: {review[1]['rating']}")
    #             # st.write(f"Questions: {questions}")
    #             if len(review[1]['text']) > 100:
    #                 st.write("[See more]")
    
    
def create_review_card(company_info, review_ls, question_ls):
    with st.container(border=True):
        st.write(f"### {company_info['name']} Review:")
        
        for i in range(len(review_ls)):
            st.write(f"#### Title: {review_ls[i][1]['title']}")
            st.write(review_ls[i][1]['text'])
            st.write("Questions: ")
            if 'message' in question_ls[i]:
                st.write("No questions yet!")
                continue                
            for question in question_ls[i].values():
                for i in range(len(question)):
                    for item in question[i].values():
                        st.write(item)
        

        
        
        

try:
    companies = requests.get('http://api:4000/co/companies').json()
    companies_df = pd.DataFrame(companies)
    # st.dataframe(companies_df.head()['companyID'])
    for i in range(len(companies_df)): 
        companyID = companies_df.iloc[i]['companyID']        
        reviews = requests.get(f"http://api:4000/co/companies/{companyID}/reviews").json()
        reviews = pd.DataFrame(reviews)
        
        company_info = companies_df.loc[i]
        # st.write(company_info)
        review_ls = []
        question_ls = []
        for review in reviews.iterrows():
            # st.write(review)
            reviewID = review[1]['reviewID']
            questions = requests.get(f"http://api:4000/q/questions/{reviewID}").json()

            review_ls.append(review)
            question_ls.append(questions)
            # st.write(review)
            # st.write(questions)
            # create_review_card(companies_df.loc[i], reviews)
        # st.write(review_ls)
        # st.write(question_ls)
    
        create_review_card(company_info, review_ls, question_ls)
except Exception as e:
    logger.error(f"Error rendering page: {str(e)}")
    st.error("Error loading company reviews")


# Set the header of the page
st.header('Search Reviews')