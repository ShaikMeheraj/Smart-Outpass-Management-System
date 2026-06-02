import streamlit as st

def home_page():
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url('https://www.ksrmce.ac.in/data1/images/s1.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.6);
        background-blend-mode: overlay; 
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    # Center the image
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://cdni.iconscout.com/illustration/premium/thumb/student-reading-in-college-library-illustration-download-svg-png-gif-file-formats--book-at-a-together-collegy-pack-university-illustrations-4202864.png?f=webp" style="max-width: 50%;">
        </div>
        """,
        unsafe_allow_html=True
    )
