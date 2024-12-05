import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Entities')

st.write('\n\n')

with st.form('add_company_form'):

    name = st.text_input("Company Name")
    size = st.number_input("Company Size", min_value=0.0, step=1.0)

    submit_button = st.form_submit_button("Add Company")

    if submit_button:
        if not name:
            st.error("Please enter a company name")
        elif size <= 0:
            st.error("Please enter a valid company size")
        else:
            company_data = {
                "name" : name,
                "size" : size
            }

            logger.info(f"Company form submitted with data: {company_data}")

            try:

                response = requests.post('http://api:4000/co/companies', json=company_data)
                if response.status_code == 200:
                    st.success("Company added successfully!")
                else:
                    st.error(f"Error adding company: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

with st.form('add_college_form'):

    name = st.text_input("College Name")

    submit_button = st.form_submit_button("Add College")

    if submit_button:
        if not name:
            st.error("Please enter a college name")
        else:
            college_data = {
                "name" : name
            }

            logger.info(f"College form submitted with data: {college_data}")

            try:

                response = requests.post('http://api:4000/col/colleges', json=college_data)
                if response.status_code == 200:
                    st.success("College added successfully!")
                else:
                    st.error(f"Error adding college: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

with st.form('add_industry_form'):

    name = st.text_input("Industry Name")

    submit_button = st.form_submit_button("Add Industry")

    if submit_button:
        if not name:
            st.error("Please enter the name of an industry")
        else:
            industry_data = {
                "name" : name
            }

            logger.info(f"industry form submitted with data: {industry_data}")

            try:

                response = requests.post('http://api:4000/i/industries', json=industry_data)
                if response.status_code == 200 or response.status_code == 201:
                    st.success("Industry added successfully!")
                else:
                    st.error(f"Error adding industry: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    companyData = requests.get('http://api:4000/co/companies').json()

    st.dataframe(companyData)

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

with st.form('add_position_form'):

    companyID = st.selectbox("Company ID", options=companies_id_options, index=0)
    name = st.text_input("Position Name")
    description = st.text_area("Position Description")
    remote = st.selectbox("Is Position Remote?", options=[False, True], index=0)

    submit_button = st.form_submit_button("Add Position")

    if submit_button:
        if not companyID:
            st.error("Please select the company ID of the company this position belongs to")
        elif not name:
            st.error("Please enter the name of the position")
        elif not description:
            st.error("Please enter the description of the position")
        else:
            position_data = {
                "companyID" : companyID,
                "name" : name,
                "description" : description,
                "remote" : remote
            }

            logger.info(f"Position form submitted with data: {position_data}")

            try:

                response = requests.post('http://api:4000/po/positions', json=position_data)
                if response.status_code == 200 or response.status_code == 201:
                    st.success("Position added successfully!")
                else:
                    st.error(f"Error adding position: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")