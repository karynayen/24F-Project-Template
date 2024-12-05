import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Remove Entities')

st.write('\n\n')

try:
    response = requests.get('http://api:4000/q/questions').json()

    st.dataframe(response)

    questions_response = requests.get('http://api:4000/q/questionIds')

    if questions_response.status_code == 200:
        questions_data = questions_response.json()
        questions_id_options = [""] + [questionId['value'] for questionId in questions_data]

    else:
        st.error("Failed to fetch question IDs")
        questions_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to question API: {str(e)}")
    questions_id_options = []

with st.form('delete_question_form'):

    questionId = st.selectbox("Question ID", options=questions_id_options, index=0)

    submit_button = st.form_submit_button("Delete Question")

    if submit_button:
        if not questionId:
            st.error("Please select the question ID of the question you would like to delete")
        else:
            question_data = {
                "questionId" : questionId
            }

            logger.info(f"Question removal form submitted with data: {question_data}")

            try:

                response = requests.delete(f'http://api:4000/q/questions/{questionId}', json=question_data)
                if response.status_code == 200:
                    st.success("Question removed successfully!")
                else:
                    st.error(f"Error removing question: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    response = requests.get('http://api:4000/a/answers').json()

    st.dataframe(response)

    answers_response = requests.get('http://api:4000/a/answerIds')

    if answers_response.status_code == 200:
        answers_data = answers_response.json()
        answers_id_options = [""] + [answerId['value'] for answerId in answers_data]

    else:
        st.error("Failed to fetch answer IDs")
        answers_id_options = []

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to answer API: {str(e)}")
    answers_id_options = []

with st.form('delete_answer_form'):

    answerId = st.selectbox("Answer ID", options=answers_id_options, index=0)

    submit_button = st.form_submit_button("Delete Answer")

    if submit_button:
        if not answerId:
            st.error("Please select the answer ID of the answer you would like to delete")
        else:
            answer_data = {
                "answerId" : answerId
            }

            logger.info(f"Answer removal form submitted with data: {answer_data}")

            try:

                response = requests.delete(f'http://api:4000/a/answers/{answerId}', json=answer_data)
                if response.status_code == 200:
                    st.success("Answer removed successfully!")
                else:
                    st.error(f"Error removing answer: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

try:
    response = requests.get('http://api:4000/co/companies').json()

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

with st.form('delete_company_form'):

    companyID = st.selectbox("Company ID", options=companies_id_options, index=0)

    submit_button = st.form_submit_button("Delete Company")

    if submit_button:
        if not companyID:
            st.error("Please select the company ID of the company you would like to delete")
        else:
            company_data = {
                "companyID" : companyID
            }

            logger.info(f"Company removal form submitted with data: {company_data}")

            try:

                response = requests.delete(f'http://api:4000/co/companies/{companyID}', json=company_data)
                if response.status_code == 200:
                    st.success("Company removed successfully!")
                else:
                    st.error(f"Error removing company: {response.text}")
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

with st.form('delete_college_form'):

    collegeID = st.selectbox("College ID", options=colleges_id_options, index=0)

    submit_button = st.form_submit_button("Delete College")

    if submit_button:
        if not collegeID:
            st.error("Please select the college ID of the college you would like to delete")
        else:
            college_data = {
                "collegeID" : collegeID
            }

            logger.info(f"College removal form submitted with data: {college_data}")

            try:

                response = requests.delete(f'http://api:4000/col/colleges/{collegeID}', json=college_data)
                if response.status_code == 200:
                    st.success("College removed successfully!")
                else:
                    st.error(f"Error removing answer: {response.text}")
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

with st.form('delete_industry_form'):

    industryID = st.selectbox("Industry ID", options=industries_id_options, index=0)

    submit_button = st.form_submit_button("Delete Industry")

    if submit_button:
        if not industryID:
            st.error("Please select the industry ID of the industry you would like to delete")
        else:
            industry_data = {
                "industryID" : industryID
            }

            logger.info(f"Industry removal form submitted with data: {industry_data}")

            try:

                response = requests.delete(f'http://api:4000/i/industries/{industryID}', json=industry_data)
                if response.status_code == 200:
                    st.success("Industry removed successfully!")
                else:
                    st.error(f"Error removing industry: {response.text}")
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

with st.form('delete_position_form'):

    positionID = st.selectbox("Position ID", options=positions_id_options, index=0)

    submit_button = st.form_submit_button("Delete Position")

    if submit_button:
        if not positionID:
            st.error("Please select the position ID of the position you would like to delete")
        else:
            position_data = {
                "positionID" : positionID
            }

            logger.info(f"Position removal form submitted with data: {position_data}")

            try:

                response = requests.delete(f'http://api:4000/po/positions/{positionID}', json=position_data)
                if response.status_code == 200:
                    st.success("Position removed successfully!")
                else:
                    st.error(f"Error removing position: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")