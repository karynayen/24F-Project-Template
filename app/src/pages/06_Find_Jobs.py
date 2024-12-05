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

# Set the header of the page
st.header('Company Reviews')
           



# Fetch company data from API
companies = requests.get('http://api:4000/co/companies')
companies.raise_for_status()
companies = companies.json()
companies_df = pd.DataFrame(companies)

# Get reviews associated with each company
for row in companies_df.iterrows():
    companyID = row[1][0]
    reviews = pd.DataFrame(requests.get(f"http://api:4000/co/companies/{companyID}/reviews").json()).loc[:, ['title', 'text', 'reviewID', 'rating']]
    
    # Create expanders for each company
    company_name = row[1][1]
    size = row[1][2]
    with st.expander(f"### **{company_name}** -Click to expand", expanded=False):
        st.write(f"Size: {size}")
        for review in reviews.iterrows():
            with st.container(border=True):
                st.write(f"**Title:** {review[1][0]}")
                st.write(f"**Review:** {review[1][1]}")
                st.write(f"**Rating:** {review[1][3]}/5")

