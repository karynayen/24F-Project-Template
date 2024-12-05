from venv import logger
import streamlit as st
import requests
from requests.exceptions import ConnectionError
from modules.nav import SideBarLinks

SideBarLinks()

def get_reviewer_id_by_name(author_name):
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

def get_reviews_by_reviewer_id(reviewer_id):
    try:
        response = requests.get(f'http://api:4000/r/reviews?authorID={reviewer_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch reviews: {e}")
        return []

def delete_review(review_id):
    try:
        response = requests.delete(f'http://api:4000/r/reviews/{review_id}')
        response.raise_for_status()
        st.success("Review deleted successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete review: {e}")

def update_review(review_id, review_data):
    try:
        response = requests.put(f'http://api:4000/r/reviews/{review_id}', json=review_data)
        response.raise_for_status()
        st.success("Review updated successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update review: {e}")

def main():
    st.title("Your Reviews")
    
    author_name = "Ally Descoteaux"
    reviews = get_reviews_by_reviewer_id(1)
        
    if reviews:
            for review in reviews:
                st.subheader(f"Review ID: {review['reviewID']}")
                title = st.text_input("Review Title:", value=review['title'], key=f"title_{review['reviewID']}")
                rating = st.slider("Rating:", min_value=0, max_value=5, value=review['rating'], key=f"rating_{review['reviewID']}")
                recommend = st.checkbox("Recommend", value=review['recommend'], key=f"recommend_{review['reviewID']}")
                pay_type = st.selectbox("Pay Type:", ["hourly", "salary"], index=["hourly", "salary"].index(review['pay_type']), key=f"pay_type_{review['reviewID']}")
                pay = st.number_input("Pay:", min_value=0.0, format="%.2f", value=review['pay'], key=f"pay_{review['reviewID']}")
                job_type = st.selectbox("Job Type:", ["Internship", "Co-op", "Full-time", "Part Time", "Other"])
                text = st.text_area("Review Text:", value=review['text'], key=f"text_{review['reviewID']}")
                
                if st.button(f"Delete Review {review['reviewID']}", key=f"delete_{review['reviewID']}"):
                    delete_review(review['reviewID'])

                if st.button(f"Update Review {review['reviewID']}", key=f"update_{review['reviewID']}_button"):
                    review_data = {
                        "title": title,
                        "rating": rating,
                        "recommend": recommend,
                        "pay_type": pay_type,
                        "pay": pay,
                        "job_type": job_type,
                        "text": text,
                        "verified": review['verified']
                    }
                    logger.info(review_data)
                    update_review(review['reviewID'], review_data)

if __name__ == "__main__":
    main()