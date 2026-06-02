import streamlit as st
from adminstrator import admin_home_page
from staff import staff_home_page
from security import security_home_page
def user_home_page():
    # Navigation menu for user dashboard
    user_data = st.session_state.get('user', None)
    if user_data[3]=='Student':
        admin_home_page()
    if user_data[3]=='Faculty':
        staff_home_page()
    if user_data[3]=='Security':
        security_home_page()