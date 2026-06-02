import streamlit as st
from streamlit_option_menu import option_menu
import cv2
from deepface import DeepFace
import tempfile
import os
from db_manager import add_outpass,fetch_outpass,fetch_all_outpass,update_outpass
import numpy as np
import face_recognition
import base64
import sqlite3
import pandas as pd
import pygame
import time
pygame.mixer.init()
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_alert_email(to_email, subject, message, from_email, from_password):
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        pass

ALARM_SOUND = './alerm.mp3'  # Path to your buzzer sound file
def play_buzzer():
    pygame.mixer.music.load(ALARM_SOUND)
    pygame.mixer.music.play()
    time.sleep(5)  
    pygame.mixer.music.stop()

def fetch_registered_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, role, category, email, student_image FROM users WHERE student_image IS NOT NULL")
    users = cursor.fetchall()
    conn.close()

    known_face_encodings = []
    known_face_details = []  # Store (name, role, category, email)

    for user in users:
        name, role, category, email, image_data = user
        if image_data:
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_details.append((name, role, category, email))  # Include email for tracking

    return known_face_encodings, known_face_details

user_data = st.session_state.get('user', None)
CSV_FILE = "student_outpass.csv"  # Path to store student outpass attempts
def load_or_initialize_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["email", "count"])  # Create empty DataFrame if CSV doesn't exist

# Function to update CSV (only for students who are hostellers)
def update_csv(email):
    df = load_or_initialize_csv()
    to_email='shaikmeheraj308@gmail.com'
    subject = "Outperson Alert"
    body = f"Hello,\n\nThis is an alert for the student with email {email} trying to go out of the campus.\n\nPlease take necessary action.\n\nBest regards,\nYour Security System"
    from_email = 'dont.reply.mail.mail@gmail.com'
    from_password = 'ekdbgizfyaiycmkv'  
    # Send the alert email
    send_alert_email(to_email, subject, body, from_email, from_password)
    if email in df["email"].values:
        df.loc[df["email"] == email, "count"] += 1
    else:
        new_entry = pd.DataFrame({"email": [email], "count": [1]})
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)

def security_home_page():
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
                        <p><strong style="color:green;">Name:</strong> <span style="color:black;">{user_data[1]}</span></p>
                        <p><strong style="color:green;">User Type:</strong> <span style="color:black;">{user_data[3]}</span></p>
                        <p><strong style="color:green;">Email:</strong> <span style="color:black;">{user_data[2]}</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    def exam_monitor():
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://img.freepik.com/premium-photo/creative-educational-sketch-white-backdrop-with-copybooks-education-knowledge-concept-3d-rendering_670147-66821.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
        uploaded_video = st.file_uploader("📂 Upload a video", type=["mp4", "avi", "mov"])
        if uploaded_video:
            temp_dir = tempfile.TemporaryDirectory()
            video_path = os.path.join(temp_dir.name, "uploaded_video.mp4")

            with open(video_path, "wb") as f:
                f.write(uploaded_video.read())

            st.success("✅ Video uploaded successfully!")

            # Load registered users' images from the database
            known_face_encodings, known_face_details = fetch_registered_users()

            # Track detected emails to prevent multiple increments per video
            detected_emails = set()

            # Open the uploaded video
            video_capture = cv2.VideoCapture(video_path)
            stframe = st.empty()

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name, role, category, email = "Unknown", "Unknown", "Unknown", None

                    if True in matches:
                        match_index = np.argmin(face_recognition.face_distance(known_face_encodings, face_encoding))
                        name, role, category, email = known_face_details[match_index]

                    # Display role and category for all identified persons
                    display_text = f"{name} ({role})"
                    if role.lower() == "student":
                        display_text += f" - {category}"

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, display_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    # Update CSV only once per video for each detected hosteller student
                    if role.lower() == "student" and category.lower() == "hosteller" and email and email not in detected_emails:
                        update_csv(email)
                        detected_emails.add(email)
                        play_buzzer()

                stframe.image(frame, channels="BGR")

            video_capture.release()
            temp_dir.cleanup()
            st.success("🎉 Video processing complete!")

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
        outpass=fetch_all_outpass()
        pending=[]
        outpass=fetch_all_outpass()
        for i in range(0,len(outpass)):
            if outpass[i][6]=='1':
                pending.append(outpass[i])
        st.markdown(
            """
            <style>
            .container {
                background-image: url('https://img.freepik.com/free-vector/blue-curve-background_53876-113112.jpg');
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
                        <p class="title">Grant Permission for Leave Request</p>
                        <p class="info"><strong>Email:</strong> {email}</p>
                        <p class="info"><strong>Type:</strong> {leave_type if leave_type else 'N/A'}</p>
                        <p class="info"><strong>Reason:</strong> {reason if reason else 'N/A'}</p>
                        <p class="info"><strong>From:</strong> {start_date}</p>
                        <p class="info"><strong>To:</strong> {end_date}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col1,col2,col3=st.columns([3,4,1])
                # Approve button
                if col2.button(f"CLEAR OUTPASS", key=f"APPROVE-{leave_id}",type='primary'):
                    st.success(f"Outpass Cleared for {email}")
                    update_outpass(leave_id,3)
                    # Call your approval function here
                
        else:
            st.image("https://onesala.com/_nuxt/no-data-found-21.f5505e35.svg",use_column_width=True)
    # Navigation menu for user dashboard
    selected_tab = option_menu(
        menu_title=None,
        options=["Student Monitoring", "Outpass",'Logout'],
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
    if selected_tab == "Student Monitoring":
        exam_monitor()
    elif selected_tab == "Outpass":
        management()
    elif selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()
        st.rerun()