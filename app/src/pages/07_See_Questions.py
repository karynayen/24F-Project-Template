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

logger = logging.getLogger(__name__)

# Call the SideBarLinks from the nav module
SideBarLinks()
def create_review_card(company, review_data, questions):
    
    
    # Make review card
    with st.container(border=True):
        for review in reviews:
            
            with st.container(border=True):
                st.write(f"### {company['name']} Review:")
                st.write(f"**{review['name']}** - {review['title']}")
                st.write(review['text'])
                st.write(f"Pay type: {review['pay_type']}.")
                st.write(f"Pay rate: {review['pay']}")
                st.write(f"Rating: {review['rating']}")
                # st.write(f"Questions: {questions}")
                if len(review['text']) > 100:
                    st.write("[See more]")

try:
    companies = requests.get('http://api:4000/co/companies').json()
    for company in companies: 
        reviews = requests.get(f"http://api:4000/r/reviews/{company['companyID']}").json()
        for review in reviews:
            questions = requests.get(f"http://api:4000/q/questions/{review['reviewID']}").json()
            create_review_card(company, reviews, questions)
    
    
    
except Exception as e:
    logger.error(f"Error rendering page: {str(e)}")
    st.error("Error loading company reviews")


# Set the header of the page
st.header('Search Reviews')