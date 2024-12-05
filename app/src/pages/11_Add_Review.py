import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

def get_company_names():
    try:
        response = requests.get('http://api:4000/co/companies')
        response.raise_for_status()
        companies = response.json()
        unique_company_names = {company['name'] for company in companies}
        return sorted(list(unique_company_names))
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch company data: {e}")
        return []

def get_company_id_by_name(company_name):
    try:
        response = requests.get(f'http://api:4000/co/companies?name={company_name}')
        response.raise_for_status()
        company_data = response.json()
        if company_data:
            return company_data[0]['companyID']
        else:
            st.error("Company not found")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch company data: {e}")
        return None

def get_all_positions():
    try:
        response = requests.get('http://api:4000/po/positions')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch positions: {e}")
        return []

def get_position_id_by_name(position_name):
    try:
        response = requests.get(f'http://api:4000/po/positions?name={position_name}')
        response.raise_for_status()
        position_data = response.json()
        if position_data:
            return position_data[0]['positionID']
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch position data: {e}")
        return None

def get_author_id_by_name(author_name):
    try:
        response = requests.get(f'http://api:4000/rver/reviewers?name={author_name}')
        response.raise_for_status()
        author_data = response.json()
        if author_data:
            return author_data[0]['reviewerID']
        else:
            st.error("Reviewer not found")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch reviewer data: {e}")
        return None

def add_review(review_data):
    try:
        response = requests.post('http://api:4000/r/reviews', json=review_data)
        response.raise_for_status()
        st.success("Review added successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add review: {e}")

def main():
    st.title("Add a Review")
    
    company_names = get_company_names()
    if not company_names:
        return
    
    company_name = st.selectbox("Select Company", company_names)
    company_id = get_company_id_by_name(company_name)
    
    if company_id:
        positions = get_all_positions()
        position_names = [position['name'] for position in positions]
        selected_position = st.selectbox("Select Position", position_names)
        
        position_name = selected_position
        remote = False
        
        author_name = "Ally Descoteaux"
        title = st.text_input("Review Title:")
        num_co_op = st.number_input("Number of Co-ops:", min_value=0)
        rating = st.slider("Rating:", min_value=0, max_value=5)
        recommend = st.checkbox("Recommend")
        pay_type = st.selectbox("Pay Type:", ["hourly", "salary"])
        pay = st.number_input("Pay:", min_value=0.0, format="%.2f")
        job_type = st.selectbox("Job Type:", ["Internship", "Co-op", "Full-time", "Part Time", "Other"])
        text = st.text_area("Review Text:")
        verified = 0
        
        if st.button("Submit Review"):
            position_id = get_position_id_by_name(position_name)
            
            if position_id:
                author_id = get_author_id_by_name(author_name)
                if author_id:
                    review_data = {
                        "companyID": company_id,
                        "positionID": position_id,
                        "authorID": author_id,
                        "title": title,
                        "num_co-op": num_co_op,
                        "rating": rating,
                        "recommend": int(recommend),  # Convert boolean to integer
                        "pay_type": pay_type,
                        "pay": pay,
                        "job_type": job_type,
                        "text": text,
                        "verified": int(verified)  # Convert boolean to integer
                    }
                    add_review(review_data)

if __name__ == "__main__":
    main()
