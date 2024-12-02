import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Accessing a REST API from Within Streamlit")

"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""
data = {} 
try:
  data = requests.get('http://api:4000/data').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(data)

# New section to test positions routes
st.write("## Positions Data")

positions_data = {}
try:
    positions_data = requests.get('http://api:4000/po/positions').json()
except:
    st.write("**Important**: Could not connect to positions API, so using dummy data.")
    positions_data = [
        {"positionID": 1, "companyID": 1, "name": "Software Engineer", "description": "Develop and maintain software applications", "remote": True},
        {"positionID": 2, "companyID": 2, "name": "Data Analyst", "description": "Analyze and interpret complex data sets", "remote": False}
    ]

st.dataframe(positions_data)

# New section to test colleges routes
st.write("## Colleges Data")

colleges_data = {}
try:
    colleges_data = requests.get('http://api:4000/co/colleges').json()
except:
    st.write("**Important**: Could not connect to colleges API, so using dummy data.")
    colleges_data = [
        {"collegeID": 1, "name": "Evergreen State University"},
        {"collegeID": 2, "name": "Redwood Technical Institute"}
    ]

st.dataframe(colleges_data)
