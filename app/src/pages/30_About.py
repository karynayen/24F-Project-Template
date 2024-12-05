import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About Glasshusky")

st.markdown (
    """
    When it comes to job review sites like Glassdoor, there is very little information targeted towards 
    Co-ops. Co-op seekers are a very specific demographic whose experience may largely differ from a 
    normal full-time Employee. We aim to fill this gap in the market with our new product: GlassHusky. 

    
    Imagine a Co-op review platform that goes beyond standard ratings to provide co-op seekers with 
    actionable insights about their potential workplaces. Our app is designed to empower students by 
    offering a comprehensive, data-driven view of internship experiences across industries. While existing 
    platforms like Glassdoor provide general company ratings, they often overlook the unique challenges and
    expectations of Co-ops. Co-ops frequently face limited access to information on workplace culture,
    mentorship quality, and skill-building opportunities specific to early-career roles. Our platform closes
    this gap, giving students and young professionals the detailed guidance they need to make informed 
    choices.

    We’re building this app for Co-op seekers who need transparent, authentic information; Co-op reviewers 
    who want to share their experiences; and Northeastern University administrators aiming to gain deeper 
    insights into Co-op companies and student trends. Key features include:
    - Star rating
    - Comments
    - Data visualizations
        - Company ratings across different industries
        - Num of former co-ops and reviews 
        - etc.
    - Searching
    - q&a section for each company

    Our platform provides a much-needed bridge between students and co-ops, helping the next generation of 
    talent find the right place to grow.
    """
        )
