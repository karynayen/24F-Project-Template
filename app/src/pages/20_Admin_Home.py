import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Add New Company Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Add_Company.py')

if st.button('Update Existing Company Profile',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Update_Company.py')

if st.button('Remove Existing Questions and Answers',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Remove_Questions_Answers.py')