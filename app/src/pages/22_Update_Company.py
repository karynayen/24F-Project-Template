import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Update Company Profile Page')

st.write('\n\n')

try:
    companies_response = requests.get('http://api:4000/com/companyID')

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
    size = st.text_input("Company Size", min_value=0.0, step=1.0)
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

                response = requests.put(f'http://api:4000/com/companies/{companyID}', json=company_data)
                if response.status_code == 200:
                    st.success("Company updated successfully!")
                else:
                    st.error(f"Error updating company: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")