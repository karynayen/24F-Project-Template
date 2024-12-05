import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Update Entities')

st.write('\n\n')

try:
    response = requests.get('http://api:4000/co/companies_simple').json()

    st.dataframe(response)

    companies_response = requests.get('http://api:4000/co/companyIDs')

    if companies_response.status_code == 200:
        companies_data = companies_response.json()
        companies_id_options = [""] + [companyID['value'] for companyID in companies_data]

    else:
        st.error("Failed to fetch company IDs")
        companies_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to company API: {str(e)}")
    companies_id_options = []

with st.form('update_company_form'):

    name = st.text_input("Company Name")
    size = st.number_input("Company Size", min_value=0.0, step=1.0)
    companyID = st.selectbox("Company ID", options=companies_id_options, index=0)

    submit_button = st.form_submit_button("Update Company")

    if submit_button:
        if not name:
            st.error("Please enter an updated company name")
        elif size <= 0:
            st.error("Please enter a valid, updated company size")
        elif not companyID:
            st.error("Please select the company ID of the company you would like to update")
        else:
            company_data = {
                "name" : name,
                "size" : size,
                "companyID" : companyID
            }

            logger.info(f"Company update form submitted with data: {company_data}")

            try:

                response = requests.put(f'http://api:4000/co/companies/{companyID}', json=company_data)
                if response.status_code == 200:
                    st.success("Company updated successfully!")
                else:
                    st.error(f"Error updating company: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    response = requests.get('http://api:4000/col/colleges').json()

    st.dataframe(response)

    colleges_response = requests.get('http://api:4000/col/collegeIDs')

    if colleges_response.status_code == 200:
        colleges_data = colleges_response.json()
        colleges_id_options = [""] + [collegeID['value'] for collegeID in colleges_data]

    else:
        st.error("Failed to fetch college IDs")
        colleges_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to college API: {str(e)}")
    colleges_id_options = []

with st.form('update_college_form'):

    name = st.text_input("College Name")
    collegeID = st.selectbox("College ID", options=colleges_id_options, index=0)

    submit_button = st.form_submit_button("Update College")

    if submit_button:
        if not name:
            st.error("Please enter an updated college name")
        elif not collegeID:
            st.error("Please select the college ID of the college you would like to update")
        else:
            college_data = {
                "name" : name,
                "collegeID" : collegeID
            }

            logger.info(f"College update form submitted with data: {college_data}")

            try:

                response = requests.put(f'http://api:4000/col/colleges/{collegeID}', json=college_data)
                if response.status_code == 200:
                    st.success("College updated successfully!")
                else:
                    st.error(f"Error updating college: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    response = requests.get('http://api:4000/i/industries').json()

    st.dataframe(response)

    industries_response = requests.get('http://api:4000/i/industryIDs')

    if industries_response.status_code == 200:
        industries_data = industries_response.json()
        industries_id_options = [""] + [industryID['value'] for industryID in industries_data]

    else:
        st.error("Failed to fetch industry IDs")
        industries_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to industry API: {str(e)}")
    industries_id_options = []

with st.form('update_industry_form'):

    name = st.text_input("Industry Name")
    industryID = st.selectbox("Industry ID", options=industries_id_options, index=0)

    submit_button = st.form_submit_button("Update Industry")

    if submit_button:
        if not name:
            st.error("Please enter an updated industry name")
        elif not industryID:
            st.error("Please select the industry ID of the industry you would like to update")
        else:
            industry_data = {
                "name" : name,
                "industryID" : industryID
            }

            logger.info(f"Industry update form submitted with data: {industry_data}")

            try:

                response = requests.put(f'http://api:4000/i/industries', json=industry_data)
                if response.status_code == 200:
                    st.success("Industry updated successfully!")
                else:
                    st.error(f"Error updating industry: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    response = requests.get('http://api:4000/po/positions').json()

    st.dataframe(response)

    positions_response = requests.get('http://api:4000/po/positionIDs')

    if positions_response.status_code == 200:
        positions_data = positions_response.json()
        positions_id_options = [""] + [positionID['value'] for positionID in positions_data]

    else:
        st.error("Failed to fetch position IDs")
        positions_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to position API: {str(e)}")
    positions_id_options = []

with st.form('update_position_form'):

    name = st.text_input("Position Name")
    description = st.text_area("Position Description")
    remote = st.selectbox("Is Position Remote?", options=[False, True], index=0)
    positionID = st.selectbox("Position ID", options=positions_id_options, index=0)

    submit_button = st.form_submit_button("Update Position")

    if submit_button:
        if not name:
            st.error("Please enter an updated position name")
        elif not description:
            st.error("Please enter an updated position description")
        elif not positionID:
            st.error("Please select the position ID of the position you would like to update")
        else:
            position_data = {
                "name" : name,
                "description" : description,
                "remote" : remote,
                "positionID" : positionID
            }

            logger.info(f"Position update form submitted with data: {position_data}")

            try:

                response = requests.put(f'http://api:4000/po/positions/{positionID}', json=position_data)
                if response.status_code == 200:
                    st.success("Position updated successfully!")
                else:
                    st.error(f"Error updating position: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")