import streamlit as st
import cv2
import numpy as np
import face_recognition
import sqlite3
import tempfile
import os
import pandas as pd

CSV_FILE = "student_outpass.csv"  # Path to store student outpass attempts

# Function to fetch registered users (name, role, category, email, image)
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

# Function to load or initialize CSV
def load_or_initialize_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["email", "count"])  # Create empty DataFrame if CSV doesn't exist

# Function to update CSV (only for students who are hostellers)
def update_csv(email):
    df = load_or_initialize_csv()

    if email in df["email"].values:
        df.loc[df["email"] == email, "count"] += 1
    else:
        new_entry = pd.DataFrame({"email": [email], "count": [1]})
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)

# Streamlit UI
st.title("🎥 Face Recognition from Uploaded Video")

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

        stframe.image(frame, channels="BGR")

    video_capture.release()
    temp_dir.cleanup()
    st.success("🎉 Video processing complete!")
