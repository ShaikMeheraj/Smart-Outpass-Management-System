import streamlit as st
from login_page import login_page
from register_page import register_page
from db_manager import init_db
from streamlit_option_menu import option_menu
from home_page import home_page
from features_page import features_page
from user_home import user_home_page

# Initialize the database
init_db()

# Streamlit Page Config
st.set_page_config(page_title = 'Outpass Management', layout='wide', page_icon="🛂")

# Add background image to the main page

# Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if st.session_state["page"] == "Home":
    # Horizontal navigation for non-logged-in users
    st.markdown(
        """
        <div style="text-align: center; padding: 1px; background-color: pink; border-radius: 40px; border: 1.5px solid black; margin-bottom: 20px;">
            <p style="color: black; font-size: 40px;"><b>Smart College Outpass Management System</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Login", "Register",'Features'],
        icons=["house", "box-arrow-in-right", "person-plus",'info-circle'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "nav-link-selected": {
                "background-color": "#ffc11c",  # Background color of the selected item
                "color": "black",
            },
            "nav-link": {
                "background-color": "#ffefc4",  # Background color of unselected items
                "color": "black",  # Text color of unselected items
            },
        },
    )

    # Render the selected page
    if selected_page == "Home":
        home_page()
    elif selected_page == "Login":
        #clear session state
        login_page()
    elif selected_page == "Register":
        register_page()
    elif selected_page == "Features":
        features_page()

elif st.session_state["page"] == "user_home":
    # Redirect to the user dashboard after login
    user_home_page()
    #clear session state
