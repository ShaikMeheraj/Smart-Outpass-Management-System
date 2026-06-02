import streamlit as st
import re
from db_manager import register_user

def register_page():
    # Center the registration form container using Streamlit form layout
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://img.freepik.com/free-vector/bokeh-bubbles-sun-flash-blue-background_1182-1745.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.form(key="register_form"):
        # Title
        st.title("Sign Up Here!!")
        # Form Fields
        col1, col2 = st.columns(2)
        name = col1.text_input("Name")
        email = col2.text_input("Email")
        role = col1.selectbox("Role", ["Student", "Faculty", "Security"])
        branch = col2.selectbox("Branch", ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIML", "None"],index=  7)
        col1, col2 = st.columns(2)
        student_image = col2.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        category=col1.selectbox("Category",["Hosteller",'Others'],index=0)
        col1, col2 = st.columns(2)
        password = col1.text_input("Password", type="password")
        retype_password = col2.text_input("Retype Password", type="password")

        # Submit Button inside the form
        register_button = st.form_submit_button("Register")

        # Handling form submission
        if register_button:
            # Validate email using regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                st.error("Invalid Email!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif password != retype_password:
                st.error("Passwords do not match!")
            else:
                if register_user(name, email, role, branch, student_image, category, password):
                    st.success("Registration Successful!")
                else:
                    st.error("Email already exists!")
