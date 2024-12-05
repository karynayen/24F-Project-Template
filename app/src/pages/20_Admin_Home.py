import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Add New Company Profile, College, Industry, Or Position', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Add_Entity.py')

if st.button('Update Existing Company Profile, College, Industry, Or Position',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Update_Entity.py')

if st.button('Remove Existing Questions, Answers, Company Profiles, Colleges, Industries, Or Positions',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Remove_Entity.py')