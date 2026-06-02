import streamlit as st
from db_manager import validate_user,fetch_all_users

def login_page():
    # Center the login form using Streamlit form layout
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://img.freepik.com/free-vector/pink-green-background-design_23-2150304126.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    col1,col2,col3=st.columns([9,10,5])
    # Title
    col2.title("Login Here!!")
    users=fetch_all_users()
    
    # Email and Password inputs
    col1, col2, col3 = st.columns([1, 3, 1])
    email = col2.text_input("Enter Email")
    password = col2.text_input("Enter Password", type="password")
    col1, col2, col3 = st.columns([12, 10, 5])
    # Submit button inside the form
    login_button = col2.button("Login")
    col1, col2, col3 = st.columns([1, 3, 1])
    #clear session state
    # Handling form submission
    try:
        if login_button:
            user = validate_user(email, password)
            if user:
                # Set session state to user_home and store user details
                st.session_state["page"] = "user_home"
                st.session_state["user"] = user  # Store user info (e.g., name, email)
                st.session_state["user_tab"] = "Loan Page"  # Default tab after login
                st.experimental_rerun()
            else:
                col2.error("Invalid email or password!")
    except Exception as e:
        col2.error("An error occurred: " + str(e))
