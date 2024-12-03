import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Company')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# # get the countries from the world bank data
# with st.echo(code_location='above'):
#     countries:pd.DataFrame = wb.get_countries()
   
#     st.dataframe(countries)

# # the with statment shows the code for this block above it 
# with st.echo(code_location='above'):
#     arr = np.random.normal(1, 1, size=100)
#     test_plot, ax = plt.subplots()
#     ax.hist(arr, bins=20)

#     st.pyplot(test_plot)


# with st.echo(code_location='above'):
#     slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
#     data_crosstab = pd.crosstab(slim_countries['region'], 
#                                 slim_countries['incomeLevel'],  
#                                 margins = False) 
#     st.table(data_crosstab)

# ======================================================================================================================

#calling all companies
st.write("Pulling all companies")

company_df = {} 
try:
  #List of: city, companyID, country, industryname (i.name), industryID, locID, 
  #companyname (name), postcode, size, state, street 
  co_data = requests.get('http://api:4000/co/companies').json()
  company_df= pd.DataFrame(co_data)
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  company_df = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(company_df)

# Retrieve each company's ID, name, and size since there were duplicates in company_df for future iterations over the data
unique_company = company_df[['companyID', 'name', 'size']].drop_duplicates()

# ======================================================================================================================

st.write("All reviews for each company sorted by companyID")
reviews_df = pd.DataFrame()
try:
  # iterates through companyIDs and adds matching reviews to 1 large dataframe
  for id_num in unique_company['companyID']:
     response = requests.get(f'http://api:4000/co/companies/{id_num}/reviews').json()
     review = pd.DataFrame(response)
     reviews_df = pd.concat([reviews_df, review], axis =0, ignore_index = True)
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  reviews_df = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(reviews_df)

# ======================================================================================================================

#iterate through company dataframe and add in corresponding reviews
# for i in range(len(unique_coID)):
#     co_review_df = pd.DataFrame()
#     for n in range(len(reviews_df['companyID'])):
#         if unique_coID[i] == reviews_df['companyID'].iloc[n]:
#            st.write(f'{unique_coID[i]}, {reviews_df["companyID"].iloc[n]}')
#            co_review_df = pd.concat([co_review_df, reviews_df.iloc[n]], axis =1, ignore_index = True)
#     st.write(f"# {unique_company[i]}")
#     # st.write(f"### {company_df.loc[i, 'size']}") 
#     st.table(co_review_df)


st.write("## Company Information and Reviews")

# Getting company information: name, city/state, industry, size
for _, row in unique_company.iterrows():
    # Extract company details
    coID = row['companyID']
    name = row['name']
    size = row['size']

    # Filter rows for the current company
    matching_rows = company_df[company_df['companyID'] == coID]
    
    # Extract unique values for city/state and industry
    city_state = matching_rows[['city', 'state']].drop_duplicates().values.tolist()
    industry = matching_rows['i.name'].unique() 
    
   
    # Formatting data to be more readable
    st.markdown(
    f"**Company:** {name}  \n"
    f"**City/State:** {', '.join([f'{city}, {state}' for city, state in city_state])}  \n"
    f"**Industry:** {', '.join(industry)}  \n"
    f"**Size:** {size}"
)

# Matching reviews to Company

    # Initialize empty df
    co_review_df = pd.DataFrame()
    # Iterate through reviews_df
    for n in range(len(reviews_df['companyID'])):
        #match companyID from reviews_df to companyID from the unique company df
        if coID == reviews_df['companyID'].iloc[n]:
           #add review corresponding to matching company to dataframe of company reviews~ co_review_df
           co_review_df = pd.concat([co_review_df, reviews_df.iloc[n]], axis =1, ignore_index = True)
    
    # Display only specific labels which are the indices for the rows
    expected_labels = ['title', 'job_type', 'num_co-op', 'pay', 'pay_type', 'rating', 'recommend', 'text', 'verified']
    matching_rows = co_review_df.loc[expected_labels]

    # Display the selected rows
    st.table(matching_rows)
    



    
# with st.echo(code_location='above'):
#     # arr = np.random.normal(1, 1, size=100)
#     # test_plot, ax = plt.subplots()
#     # ax.hist(arr, bins=20)

#     # st.pyplot(test_plot)
#     # companies_df = pd.DataFrame(data)
#     company1_df = data[0] #data = list of companyID, Name, size
#     st.dataframe(company1_df)
