import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Company Profile Page')

st.write('\n\n')

with st.form('add_company_form'):

    name = st.text_input("Company Name")
    size = st.text_input("Company Size", min_value=0.0, step=1.0)

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

                response = requests.post('http://api:4000/com/companies', json=company_data)
                if response.status_code == 200:
                    st.success("Company added successfully!")
                else:
                    st.error(f"Error adding company: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")