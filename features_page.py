import streamlit as st

def features_page():
    # Center the login form using Streamlit form layout
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjEwNjQtMzYta3ZjNHNieHcuanBn.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    d1, d2, d3, d4, d5, d6= ["Outpass Creation", "Outpass Approval", "Security Hosteller Management", "Real-Time Monitoring", "Staff Hostellers Details", "Download Outpass for Students"]
    h1, h2, h3, h4, h5, h6 = ["Students can create an outpass request digitally, specifying the required details and reason for their leave.", 
                                       "Authorities can review and approve outpass requests efficiently through the system.", 
                                       "This feature helps security personnel manage hostellers by tracking their movements and ensuring security.", 
                                       "A real-time monitoring system keeps track of hosteller activities and provides instant updates.",
                                       "Staff can access and manage details of hostellers efficiently, improving hostel administration.",
                                       "Students can download their approved outpass for easy access and reference when leaving the hostel."]
    i1 = "https://i1.sndcdn.com/avatars-000564219648-nq2ln3-t500x500.jpg"
    i2 = "https://pix4free.org/assets/library/2021-06-16/originals/staff.jpg"
    i3 = "https://images.jdmagicbox.com//comp/service_catalogue/watchman-and-guards-service-for-factory-022pxx22.xx22.140303131235.s1z1-xhecojy.jpg"
    i4 = "https://media.istockphoto.com/id/477385972/photo/security-cctv-camera-in-office-building.jpg?s=612x612&w=0&k=20&c=0H44Pea7SjRjGfKHVL-vrmE-4SfEzquadLc2EvOhi9U="
    i5 = "https://ahduni.edu.in/site/assets/files/7325/760_x_540_amsom_faculty.1400x0.webp"
    i6 = "https://m.media-amazon.com/images/I/812H-l3gL7L.jpg"

    profile_css = """
        <style>
            .profile-container {
                background-color: #8bdaf0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                max-width: 300px;
                border: 1px solid #ccc;
                margin: 10px;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            .profile-header {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333;
            }
            .profile-item {
                font-size: 14px;
                margin-bottom: 5px;
                color: #555;
            }
            .profile-image img {
                border-radius: 30%;
                max-width: 200px;
                max-height: 200px;
                margin-bottom: 10px;
            }
        </style>
    """

    def create_profile_html(name, description, image_link):
        return f"""
        <div class="profile-container">
            <div class="profile-image">
                <img src="{image_link}" alt="Feature Image">
            </div>
            <div class="profile-details">
                <div class="profile-header"><strong>{name}</strong></div>
                <div class="profile-item">{description}</div>
            </div>
        </div>
        """

    col1, col2,col3=st.columns(3)
    col1.markdown(profile_css + create_profile_html(d1, h1, i1), unsafe_allow_html=True)
    col2.markdown(profile_css + create_profile_html(d2, h2, i2), unsafe_allow_html=True)
    col3.markdown(profile_css + create_profile_html(d3, h3, i3), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    col4.markdown(profile_css + create_profile_html(d4, h4, i4), unsafe_allow_html=True)    
    col5.markdown(profile_css + create_profile_html(d5, h5, i5), unsafe_allow_html=True)
    col6.markdown(profile_css + create_profile_html(d6, h6, i6), unsafe_allow_html=True)