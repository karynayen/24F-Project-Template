import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

def get_company_names():
    try:
        response = requests.get('http://api:4000/co/companies')
        response.raise_for_status()
        companies = response.json()
        unique_company_names = {company['name']: company['companyID'] for company in companies}
        return [{"name": name, "companyID": companyID} for name, companyID in unique_company_names.items()]
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch company data: {e}")
        return []

def get_company_reviews(company_id):
    try:
        response = requests.get(f'http://api:4000/co/companies/{company_id}/reviews')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch reviews: {e}")
        return []

def main():
    st.title("Company Reviews")
    
    company_names = get_company_names()
    if not company_names:
        return
    
    company_name = st.selectbox("Select Company", [company['name'] for company in company_names])
    company_id = next((company['companyID'] for company in company_names if company['name'] == company_name), None)
    
    if st.button("Get Reviews") and company_id:
        reviews = get_company_reviews(company_id)
        if reviews:
            for review in reviews:
                st.subheader(f"Review ID: {review['reviewID']}")
                st.write(f"Title: {review['title']}")
                st.write(f"Rating: {review['rating']}")
                st.write(f"Recommend: {review['recommend']}")
                st.write(f"Pay Type: {review['pay_type']}")
                st.write(f"Pay: {review['pay']}")
                st.write(f"Job Type: {review['job_type']}")
                st.write(f"Date: {review['date_time']}")
                st.write(f"Verified: {review['verified']}")
                st.write(f"Text: {review['text']}")
                st.write("---")

if __name__ == "__main__":
    main()
