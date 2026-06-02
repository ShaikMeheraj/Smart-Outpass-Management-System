import streamlit as st
from streamlit_option_menu import option_menu
import cv2
from deepface import DeepFace
from tempfile import NamedTemporaryFile
import os
import numpy as np
import datetime
from fpdf import FPDF
import base64
from db_manager import add_outpass,fetch_outpass,fetch_all_outpass


user_data = st.session_state.get('user', None)
def admin_home_page():
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
                        <p><strong style="color:red;">Name:</strong> <span style="color:black;">{user_data[1]}</span></p>
                        <p><strong style="color:red;">User Type:</strong> <span style="color:black;">{user_data[3]}</span></p>
                        <p><strong style="color:red;">Email:</strong> <span style="color:black;">{user_data[2]}</span></p>
                        <p><strong style="color:red;">Department:</strong> <span style="color:black;">{user_data[4]}</span></p>
                        <p><strong style="color:red;">Stay Type:</strong> <span style="color:black;">{user_data[6]}</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.error("User not logged in!")
    def exam_monitor():
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://img.freepik.com/premium-vector/best-decorative-border_1195262-4756.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        col1,col2,col3=st.columns([1,8,1])
        today = datetime.date.today()
        with col2.form(key="outpass_form"):
            subject = st.text_input("Enter Subject")
            reason=st.text_area("Enter Reason")
            from_date=st.date_input("From Date",min_value=today)
            to_date=st.date_input("To Date",min_value=today)
            statu=0
            col1,col2,col3=st.columns([3,3,1])
            button=col2.form_submit_button("Submit",type='primary')
            if button and subject and reason and from_date and to_date:
                add_outpass(user_data[2],subject,reason,from_date,to_date,statu)
                st.success("Outpass Request Submitted Successfully")
            else:
                st.error("Please Fill all the fields")
    
    def management():
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://png.pngtree.com/background/20210715/original/pngtree-white-simple-texture-background-picture-image_1323742.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
    """
    <style>
        .main {
            background-image: url('https://png.pngtree.com/background/20210715/original/pngtree-white-simple-texture-background-picture-image_1323742.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .outpass-box {
            border: 2px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            background-image: url('https://img.freepik.com/premium-vector/abstract-background-geometric-blue-green-wave-effect-with-memphis-background_586360-2484.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }
        .outpass-title {
            font-weight: bold;
            font-size: 18px;
            color: black;
        }
        .label {
            color: red;
            font-weight: bold;
        }
        .value {
            color: black;
        }
        .download-btn {
            background-color: pink;
            color: white;
            padding: 5px;
            border-radius: 60px;
            text-align: center;
            display: inline-block;
            margin-top: 1px;
            width: 20%;

        }
        .status-icon {
            position: absolute;
            right: 15px;
            top: 15px;
            width: 30px;
            height: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        # Fetch all outpasses
        all_outpass = fetch_outpass(user_data[2])
        # Categorize outpasses
        approved_outpass = []
        pending_outpass = []
        rejected_outpass = []

        for outpass in all_outpass:
            if int(outpass[6]) == 1:
                approved_outpass.append(outpass)
            elif int(outpass[6]) == 0:
                pending_outpass.append(outpass)
            elif int(outpass[6]) == 2:
                rejected_outpass.append(outpass)

        # Select box for filtering
        col1,col2=st.columns([4,1])
        col1.markdown("<h1 style='text-align: center; color: #b58709;'>Outpass Management</h1>", unsafe_allow_html=True)
        status_filter = col2.selectbox("Select Outpass Type:", ["All", "Approved", "Pending", "Rejected"], index=2)

        # Function to generate PDF report
        def generate_pdf(outpasses):
            pdf = FPDF(orientation='L')  # Set to landscape mode
            pdf.set_auto_page_break(auto=True, margin=30)
            pdf.add_page()
            pdf.set_font("Times", size=24,style='B')
            
            # Add background image
            background_image='background.jpg'
            pdf.image(background_image, x=0, y=0, w=297, h=210)
            
            pdf.set_text_color(255, 0, 0)  # Set text color to red (RGB)
            pdf.cell(200, 10, "KSRM College of Engineering", ln=True, align='C')
            pdf.set_text_color(0, 0, 0)  # Reset text color to black for the rest of the content
            pdf.ln(10)
            pdf.cell(200, 10, "Approved Outpass Report", ln=True)
            pdf.ln(10)
            pdf.set_font("Times", size=18)
            for outpass in outpasses:
                pdf.image('appr.png', x=150, y=pdf.get_y() - 3, w=80, h=80)
                pdf.cell(200, 10, f"Name: {outpass[1]}", ln=True)
                pdf.cell(200, 10, f"Reason: {outpass[2]}", ln=True)
                pdf.cell(200, 10, f"Details: {outpass[3]}", ln=True)
                pdf.cell(200, 10, f"From: {outpass[4]}", ln=True)
                pdf.cell(200, 10, f"To: {outpass[5]}", ln=True)
                
                # Add Approved Icon
                pdf.ln(20)
            #add approved ico in right side of the page
            # Save PDF
            pdf_output = "approved_outpass_report.pdf"
            pdf.output(pdf_output)
            return pdf_output

        def display_outpas(outpasses, status, icon_url):
            if outpasses:
                for outpass in outpasses:
                    st.markdown(
                        f"""
                        <div class="outpass-box">
                            <img src="{icon_url}" class="status-icon">
                            <p class="outpass-title" style="color: blue;">{status.upper()}</p>
                            <p><span class="label">Name:</span> <span class="value">{outpass[1]}</span></p>
                            <p><span class="label">Reason:</span> <span class="value">{outpass[2]}</span></p>
                            <p><span class="label">Details:</span> <span class="value">{outpass[3]}</span></p>
                            <p><span class="label">From:</span> <span class="value">{outpass[4]}</span></p>
                            <p><span class="label">To:</span> <span class="value">{outpass[5]}</span></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        # Function to display outpasses
        def display_outpasses(outpasses, status, icon_url):
            if outpasses:
                for outpass in outpasses:
                    st.markdown(
                        f"""
                        <div class="outpass-box">
                            <img src="{icon_url}" class="status-icon">
                            <p class="outpass-title" style="color: blue;">{status.upper()}</p>
                            <p><span class="label">Name:</span> <span class="value">{outpass[1]}</span></p>
                            <p><span class="label">Reason:</span> <span class="value">{outpass[2]}</span></p>
                            <p><span class="label">Details:</span> <span class="value">{outpass[3]}</span></p>
                            <p><span class="label">From:</span> <span class="value">{outpass[4]}</span></p>
                            <p><span class="label">To:</span> <span class="value">{outpass[5]}</span></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                col1,col2,col3=st.columns([1,8,1])
                col2.image("https://cdni.iconscout.com/illustration/premium/thumb/employee-is-unable-to-find-sensitive-data-illustration-download-in-svg-png-gif-file-formats--no-found-misplaced-files-business-pack-illustrations-8062128.png?f=webp",use_column_width=True, caption="No Outpasses Found")
        icons = {
            "Approved": "https://cdn-icons-png.flaticon.com/512/845/845646.png",
            "Pending": "https://static-00.iconduck.com/assets.00/pending-icon-2048x2014-xo9hfhyi.png",
            "Rejected": "https://cdn-icons-png.flaticon.com/512/753/753345.png"
        }

        # Display based on selection
        if status_filter == "All":
            display_outpas(approved_outpass, "Approved",icons["Approved"])
            display_outpas(pending_outpass, "Pending",icons["Pending"])
            display_outpas(rejected_outpass, "Rejected",icons["Rejected"])
        elif status_filter == "Approved":
            display_outpasses(approved_outpass, "Approved", icons["Approved"])
        elif status_filter == "Pending":
            display_outpasses(pending_outpass, "Pending", icons["Pending"])
        elif status_filter == "Rejected":
            display_outpasses(rejected_outpass, "Rejected", icons["Rejected"])

        # Show Download Button for Approved Outpasses
        if status_filter == "Approved" and approved_outpass:
            pdf_file = generate_pdf(approved_outpass)
            with open(pdf_file, "rb") as file:
                pdf_data = file.read()
                b64 = base64.b64encode(pdf_data).decode()
                download_link = f'<a href="data:application/octet-stream;base64,{b64}" download="approved_outpass_report.pdf"><div class="download-btn">Download Outpass</div></a>'
                st.markdown(download_link, unsafe_allow_html=True)
    
        
    # Navigation menu for user dashboard
    selected_tab = option_menu(
        menu_title=None,
        options=["Outpass Request", "Approval Outpass",'Logout'],
        icons=['camera-fill','newspaper','file-lock2-fill'], menu_icon="cast", default_index=0,
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
    if selected_tab == "Outpass Request":
        exam_monitor()
    elif selected_tab == "Approval Outpass":
        management()
    elif selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()
        st.rerun()