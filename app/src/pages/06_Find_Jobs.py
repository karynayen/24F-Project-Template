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
st.header('Search Reviews')
           
# Sidebar UI for filtering for company size
st.sidebar.header("Company Size")
company_size = st.sidebar.radio(
    "Select the size of the company:",
    options=["0", "1-499", "500-999", "1000-4999", "5000-9999", "10000+"],
    index=3
)

size_ranges = {
    "0+": (0, float("inf")),
    "0-499": (0, 500),
    "500-999": (500, 1000),
    "1000-4999": (1000, 5000),
    "5000-9999": (5000, 10000),
    "10000+": (10000, float("inf"))
}


# Fetch company data from API
companies = requests.get('http://api:4000/co/companies')
companies.raise_for_status()
companies = companies.json()
companies_df = pd.DataFrame(companies)

# Function to filter companies based on size range
def filter_companies(df, size_range):
    if size_range == "0":
        return df[df['size'] == 0]
    elif size_range == "1-499":
        return df[(df['size'] >= 1) & (df['size'] <= 499)]
    elif size_range == "500-999":
        return df[(df['size'] >= 500) & (df['size'] <= 999)]
    elif size_range == "1000-4999":
        return df[(df['size'] >= 1000) & (df['size'] <= 4999)]
    elif size_range == "5000-9999":
        return df[(df['size'] >= 5000) & (df['size'] <= 9999)]
    elif size_range == "10000+":
        return df[df['size'] >= 10000]
    else:
        return df

# Filter the dataframe based on the selected size range
companies_df = filter_companies(companies_df, company_size)

# Get reviews associated with each company
for row in companies_df.iterrows():
    companyID = row[1][0]
    reviews = pd.DataFrame(requests.get(f"http://api:4000/co/companies/{companyID}/reviews").json()).loc[:, ['title', 'text', 'reviewID', 'rating']]
    
    # st.write(reviews)

    # Create expanders for each company
    company_name = row[1][1]
    size = row[1][2]
    with st.expander(f"### {company_name} -Click to expand", expanded=False):
        st.write(f"Size: {size}")
        for review in reviews.iterrows():
            with st.container(border=True):
                st.write(f"Title: {review[1][0]}")
                st.write(f"Review: {review[1][1]}")
                st.write(f"Rating: {review[1][3]}/5")


