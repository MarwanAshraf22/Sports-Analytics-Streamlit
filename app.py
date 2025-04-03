import streamlit as st
from PIL import Image
import home
import team_report
import player_report
import injury_prediction
import personalized_plan

logo = Image.open('images/Logo.png')

st.set_page_config(page_title="Real Madrid CF History", page_icon=logo, layout='wide')


# Add custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #00529B;
        text-align: center;
    }
    .subheader {
        font-size: 24px;
        font-weight: 600;
        color: #2C3E50;
        margin-top: 30px;
    }
    .content {
        font-size: 18px;
        color: #34495E;
    }
    .video {
        width: 100%;
        height: 500px;
    }
    .sidebar .sidebar-content {
        background-color: #F7F7F7;
    }
    .card {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #fff;
    }
    .css-1l6n45h {  /* This is the class for Streamlit's main container */
        max-width: 100%;  /* This would make it use the entire width */
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Add Title and Sidebar Image
st.markdown('<div class="title">Real Madrid Club de Fútbol</div>', unsafe_allow_html=True)
st.sidebar.image(logo, use_container_width=True)

# Define the icons for each menu option
icons = {
    'Home': '🏠',
    'Team Report': '👥',
    'Player Report': '⚽',
    'Injury Prediction': '🤕',
    'Personalized Plan': '📝'
}

# Create Sidebar Menu with icons
menu = st.sidebar.selectbox(
    'Choose an option:',
    ('Home', 'Team Report', 'Player Report', 'Injury Prediction', 'Personalized Plan'),
    format_func=lambda x: f"{icons[x]} {x}"  # Add icon to the option label
)

# Display content based on menu selection
if menu == 'Home':
    home.display_home()
elif menu == 'Team Report':
    team_report.display_team_report()
elif menu == 'Player Report':
    player_report.display_player_report()
elif menu == 'Injury Prediction':
    injury_prediction.display_injury_prediction()
elif menu == 'Personalized Plan':
    personalized_plan.display_personalized_plan()