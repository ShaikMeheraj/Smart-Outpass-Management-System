import streamlit as st
import pickle
import pandas as pd
import math
from streamlit_option_menu import option_menu
from db_manager import fetch_all_outpass,fetch_all_users,update_outpass,fetch_user,fetch_users_by_branch
import base64
user_data = st.session_state.get('user', None)

def staff_home_page():
    def exam_monitor():
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://png.pngtree.com/background/20230204/original/pngtree-simple-aesthetic-background-with-floral-ornament-in-pastel-colors-picture-image_2025789.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
        pending=[]
        outpass=fetch_all_outpass()
        for i in range(0,len(outpass)):
            if outpass[i][6]=='0':
                pending.append(outpass[i])
        st.markdown(
            """
            <style>
            .container {
                background-image: url('https://i.pinimg.com/originals/30/92/54/309254c0ccca39aa127e28339af46e28.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
            }
            .title {
                font-size: 18px;
                font-weight: bold;
                color: #d9534f;
            }
            .info {
                font-size: 16px;
                color: #333;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        if len(pending) > 0:
            for leave in pending:
                leave_id, email, leave_type, reason, start_date, end_date, status = leave
                
                st.markdown(
                    f"""
                    <div class="container">
                        <p class="title">Leave Request</p>
                        <p class="info"><strong>Email:</strong> {email}</p>
                        <p class="info"><strong>Type:</strong> {leave_type if leave_type else 'N/A'}</p>
                        <p class="info"><strong>Reason:</strong> {reason if reason else 'N/A'}</p>
                        <p class="info"><strong>From:</strong> {start_date}</p>
                        <p class="info"><strong>To:</strong> {end_date}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col1,col2,col3=st.columns([1,4,1])
                # Approve button
                if col1.button(f"Approve", key=f"approve_{leave_id}",type='primary'):
                    st.success(f"Leave Request Approved ✅")
                    update_outpass(leave_id,1)
                    # Call your approval function here
                
                if col3.button(f"Reject", key=f"reject_{leave_id}",type='primary'):
                    st.error(f"Leave Request Rejected ❌")
                    # Call your rejection function here
                    update_outpass(leave_id,2)
        else:
            st.image("https://onesala.com/_nuxt/no-data-found-21.f5505e35.svg",use_column_width=True)

        
    def student_info():
        # Fetch users from the given department
        # Custom CSS for styling
        st.markdown("""
            <style>
                .user-container {
                    text-align: center;
                    border: 2px solid #ddd;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px;
                    background-image: url('https://i.pinimg.com/1200x/f8/ea/46/f8ea46e39a8057a7fde820ba4fd6c56e.jpg');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    width: 250px;
                }
                .user-container img {
                    margin-top: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }
                .user-container .label {
                    color: red;
                    font-weight: bold;
                    font-size: 16px;
                }
                .user-container .value {
                    color: black;
                    font-size: 16px;
                }
            </style>
        """, unsafe_allow_html=True)

        # Fetch users from the given department
        users = fetch_users_by_branch(user_data[4])
        df = pd.read_csv('student_outpass.csv')
        f_dept = user_data[4]

        user_list = []

        # Collect user data
        for i in range(len(df)):
            email = df['email'][i]
            user = fetch_user(email)

            if user and f_dept == user[4]:  # Ensure user exists and matches the department
                image_data = base64.b64encode(user[5]).decode()
                image_link = f"data:image/png;base64,{image_data}"
                
                user_list.append({
                    "image": image_link,
                    "name": user[1],
                    "email": email,
                    "count": df['count'][i]
                })

        # Display users in rows of 3 columns
        num_users = len(user_list)
        rows = math.ceil(num_users / 3)  # Calculate the number of rows needed

        for row in range(rows):
            cols = st.columns(3)  # Create 3 columns per row
            
            for col_index in range(3):
                user_index = row * 3 + col_index
                if user_index < num_users:  # Ensure index is within the available users
                    with cols[col_index]:
                        st.markdown(
                            f"""
                            <div class="user-container">
                                <img src="{user_list[user_index]['image']}" width="70%" />
                                <p class="label"></p> <p class="value">{user_list[user_index]['name']}</p>
                                <p class="label"></p> <p class="value" style="color:red;">{user_list[user_index]['count']} times tried to go out</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

    with st.sidebar:
        # Extracting user data from session state after successful login
        user_data = st.session_state.get('user', None)
        student_image=user_data[5]
        if isinstance(student_image, bytes):
            # Encode the binary image to base64
            image_data = base64.b64encode(student_image).decode()
            image_link = f"data:image/png;base64,{image_data}"
        elif isinstance(student_image, str) and student_image:  # In case it's a file path or URL
            try:
                # Open the image as binary if it's a valid file path
                with open(student_image, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode()
                    image_link = f"data:image/png;base64,{image_data}"
            except FileNotFoundError:
                # Default image in case file is not found
                image_link = "https://cdn-icons-png.flaticon.com/512/4042/4042356.png"
        else:
            # Default image if no image data is available
            image_link = "https://cdn-icons-png.flaticon.com/512/4042/4042356.png"
        if user_data:
            with st.sidebar:
                # Add custom CSS to center content
                st.markdown(
                    """
                    <style>
                    .center-content {
                        text-align: center;
                        margin: auto;
                    }
                    .center-image img {
                        display: block;
                        margin: auto;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Centered title                
                # Centered image
                st.markdown(
                    f"""
                    <div class="center-image">
                        <img src="{image_link}" width="250">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                #need gap
                st.markdown("<br>",unsafe_allow_html=True)
                # Centered user details
                st.markdown(
                    f"""
                    <div class="center-content">
                        <p><strong style="color:blue;">Name:</strong> <span style="color:black;">{user_data[1]}</span></p>
                        <p><strong style="color:blue;">User Type:</strong> <span style="color:black;">{user_data[3]}</span></p>
                        <p><strong style="color:blue;">Email:</strong> <span style="color:black;">{user_data[2]}</span></p>
                        <p><strong style="color:blue;">Department:</strong> <span style="color:black;">{user_data[4]}</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Navigation menu for user dashboard
    selected = option_menu(
        menu_title=None,
        options=["Approval Outpass", "Student Info", "Logout"],
        icons=['camera-fill','file-lock2-fill'], menu_icon="cast", default_index=0,
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
    if selected == "Approval Outpass":
        exam_monitor()
    elif selected == "Student Info":
        student_info()
    elif selected=='Logout':
        # setting session data to None
        st.session_state.clear()  # Clear session state to "log out"
        st.rerun()