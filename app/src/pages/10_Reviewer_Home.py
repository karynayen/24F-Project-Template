import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Reviewer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('See Your Reviews', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_See_User_Reviews.py')

if st.button('Add a Review', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Add_Review.py')

if st.button("See Company Reviews",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_See_Company_Reviews.py')