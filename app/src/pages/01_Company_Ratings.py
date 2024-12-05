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
st.header('Company Ratings')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("Here are all of the reviews for each company and a bar plot to show the rating distributions")

# Side bar for filtering companies
st.sidebar.header('User Input Parameters')

# Sidebar UI for choosing company size
st.sidebar.header("Company Size")
company_size = st.sidebar.radio(
    "Select the size of the company:",
    options=["0+", "0-499", "500-999", "1000-4999", "5000-9999", "10000+"],
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

selected_range = size_ranges[company_size]

# ======================================================================================================================

# Create the sort by dropdown
col1, col2 = st.columns([3, 1])
with col2:
    sort_by = st.selectbox(
        'Sort By:',
        ('Company Size Asc', 'Company Size Desc', 
         'Overall Rating Asc', 'Overall Rating Desc', 
         'Number of Ratings Asc', 'Number of Ratings Desc'),
        label_visibility='collapsed',
        index =2
    )

# ======================================================================================================================

# calling all companies to put data into a pandas dataframe

try:
  #List of: city, companyID, country, industryname (i.name), industryID, locID, 
  #companyname (name), postcode, size, state, street 
  co_data = requests.get('http://api:4000/co/companies').json()
  company_df= pd.DataFrame(co_data)
  filtered_co_df = company_df[(company_df["size"] >= selected_range[0]) & 
                              (company_df["size"] < selected_range[1])]
  if filtered_co_df.empty:
     st.warning("No companies found within the selected size range. Please adjust your filters.")
     st.stop()
  
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  filtered_co_df = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.dataframe(filtered_co_df)

# Retrieve each company's ID, name, and size since there were duplicates in company_df for future iterations over the data
unique_company = filtered_co_df[['companyID', 'name', 'size']].drop_duplicates()

# ======================================================================================================================

#matching company reviews with each company using companyID

#df for all reviews in the database
reviews_df = pd.DataFrame()
try:
  # iterates through companyIDs and adds matching reviews to 1 large dataframe
  for id_num in unique_company['companyID']:
     # calls the get request
     response = requests.get(f'http://api:4000/co/companies/{id_num}/reviews').json()
     review = pd.DataFrame(response)
     reviews_df = pd.concat([reviews_df, review], axis =0, ignore_index = True)
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  reviews_df = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

# st.dataframe(reviews_df)

#adding overall average rating to unique companies for sorting
or_df = reviews_df[['companyID', 'rating']]

mean_rating_ls = []
num_rating_ls = []

for _, row in unique_company.iterrows():
    coID = row['companyID']
    ratings_df = or_df[or_df['companyID'] == coID].copy()
    mean_rating_ls.append(ratings_df['rating'].mean())
    num_rating_ls.append(ratings_df['rating'].count())

unique_company['Overall Rating'] = mean_rating_ls
unique_company['num_ratings'] = num_rating_ls

 # Use the sort_by value to sort your dataframe
if sort_by == 'Company Size Desc':
    unique_company = unique_company.sort_values('size', ascending=False)
elif sort_by == 'Company Size Asc':
    unique_company = unique_company.sort_values('size', ascending=True)
elif sort_by == 'Overall Rating Desc':
    unique_company = unique_company.sort_values('Overall Rating', ascending=False)
elif sort_by == 'Overall Rating Asc':
    unique_company = unique_company.sort_values('Overall Rating', ascending=True)
elif sort_by == 'Number of Ratings Desc':
    unique_company = unique_company.sort_values('num_ratings', ascending=False)
elif sort_by == 'Number of Ratings Asc':
    unique_company = unique_company.sort_values('num_ratings', ascending=True)

    
# st.dataframe(unique_company)
# ======================================================================================================================

st.write("# Company Ratings")
# st.write()

# Getting company information: name, city/state, industry, size
rank = 1
for _, row in unique_company.iterrows():
    # Extract company details
    coID = row['companyID']
    name = row['name']
    size = row['size']
    mean_rating = row['Overall Rating']
    num_ratings = row['num_ratings']
  
    # Filter rows for the current company
    matching_rows = company_df[company_df['companyID'] == coID]
    
    # Extract unique values for city/state and industry
    city_state = matching_rows[['city', 'state']].drop_duplicates().values.tolist()
    industry = matching_rows['i.name'].unique() 
    
   
    # Formatting data to be more readable
    with st.container(border = True):
        col1, col2 = st.columns([1, 1])  # Define two columns with relative widths
        with col1:  # Left column for rank, name, and locations
            st.markdown(
                f"### **{rank}. {name}**  \n"
                f"**Locations:** {'; '.join([f'{city}, {state}' for city, state in city_state])}  "
                )
        with col2:  # Right column for size
            st.markdown(
                f"<br><br>**Overall Rating:** {mean_rating}/5", 
                unsafe_allow_html=True
                )

        col3, col4 = st.columns([1, 1])  # Create another row for industry and rating info
        with col3:  # Left column for industry
            st.markdown(
                f"**Industries:** {', '.join(industry)}  \n"
                f"**Size:** {size}"
                )
        with col4:  # Right column for overall rating
            st.markdown(
                f"**Number of Ratings:** {num_ratings}"
                )
        rank += 1

        # Matching reviews to Company

        # Initialize empty df
        co_review_df = pd.DataFrame()
            # Iterate through reviews_df
        for n in range(len(reviews_df['companyID'])):
            #match companyID from reviews_df to companyID from the unique company df
            co_review_df = reviews_df[reviews_df['companyID'] == coID].copy()

            expected_labels = ['title', 'job_type', 'num_co-op', 'pay', 'pay_type', 'rating', 
                            'recommend', 'text', 'verified']
            matching_columns = co_review_df[expected_labels]
            
            # Display the reviews with only the rows of interest
            # st.write("#### **Reviews**")
            # st.table(matching_columns)

        # Bar plots for rating distribution

        # creates 3 columnes with col2 being 2x bigger than col1 and col3 and placing plot in col2
        with st.expander("Histogram of Rating Distribution- Click to expand", expanded=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                fig, ax = plt.subplots(figsize=(4, 2))
                # x axis = rating values
                # y axis = rating value frequency
                ax.bar(matching_columns['rating'].value_counts().index, 
                    matching_columns['rating'].value_counts().values,
                    width = 0.5)
                    
                # plot design
                ax.set_title('Company Ratings')
                ax.set_xlabel('Rating')
                ax.set_ylabel('Count')
                ax.grid(axis='y')
                ax.set_xticks(matching_columns['rating'].value_counts().index)
                ax.set_ylim(0, max(matching_columns['rating'].value_counts().values) + 1)
                ax.set_xlim(0, 6)

                # displaying the plot
                st.pyplot(fig)