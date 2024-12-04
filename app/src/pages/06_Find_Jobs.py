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

# Set the header of the page
st.header('Search Reviews')

def create_company_card(company_data, reviews):
    with st.expander(f"{company_data['name']} - Click to expand", expanded=False):
        with st.container(border=True):
            # Company header with logo and name
            col1, col2 = st.columns([1, 5])
            with col1:
                if company_data['name'] == 'TechNova Solutions':
                    st.write(f"# 🌋")
            with col2:
                st.write(f"# {company_data['name']}")
                
            # Company details in columns
            col1, = st.columns(1)
            with col1:
                st.write(f"## Size")
                st.write(f"##### {company_data['size']} employees")
            
            # Reviews section
            review_count = len(reviews) if isinstance(reviews, list) else 0
            st.write(f"### Reviews ({review_count})")
            
            # Gets reviews and displays relevant info
            with st.container(border=True):
                for review in reviews:
                    with st.container(border=True):
                        st.write(f"**{review['name']}** - {review['title']}")
                        st.write(review['text'])
                        st.write(f"Pay type: {review['pay_type']}.")
                        st.write(f"Pay rate: {review['pay']}")
                        st.write(f"Rating: {review['rating']}")
                        if len(review['text']) > 100:
                            st.write("[See more]")
           

try:
    # Fetch company data from API
    companies = requests.get('http://api:4000/co/companies').json()
    
    for company in companies:
        # Fetch reviews for each company
        reviews = requests.get(f"http://api:4000/r/reviews/{company['companyID']}").json()
        
        # Create card for each company
        create_company_card(company, reviews)

except Exception as e:
    logger.error(f"Error rendering page: {str(e)}")
    st.error("Error loading company reviews")
