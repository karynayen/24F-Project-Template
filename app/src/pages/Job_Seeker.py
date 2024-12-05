import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')


SideBarLinks()

st.title(f"Welcome Job Seeker, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Find Jobs!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/36_Find_Jobs.py')
  
if st.button('Look at Questions',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/37_See_Questions.py')