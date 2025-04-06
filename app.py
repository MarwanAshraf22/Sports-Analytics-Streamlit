import streamlit as st
from PIL import Image
import home
import team_report
import player_report
import injury_prediction
import personalized_plan
import pandas as pd

# Load the logo
logo = Image.open('Images/Logo.png')

# Load the data
calendar_df = pd.read_csv('data/calendar_preprocessed.csv')
gps_df = pd.read_csv('data/gps_data_preprocessed.csv')
wellness_df = pd.read_csv('data/wellness_preprocessed.csv')
roster_df = pd.read_csv('data/roster_preprocessed.csv')

# Add custom CSS for styling
st.markdown(
    """
    <style>
    /* General styles */
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #00529B;
        text-align: center;
        padding-top: 20px;
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
    .card {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #fff;
        margin-bottom: 20px;
    }
    .video {
        width: 100%;
        height: 500px;
    }
    .sidebar .sidebar-content {
        background-color: #F7F7F7;
        padding-top: 20px;
    }

    /* Active Sidebar Item */
    .sidebar .stSelected {
        background-color: #DFF0FF;
        border-radius: 8px;
    }

    /* Make Streamlit's main container use the entire width */
    .css-1l6n45h {
        max-width: 100%;
        margin: 0 auto;
    }

    /* Card hover effect */
    .card:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transition: box-shadow 0.3s ease-in-out;
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
    format_func=lambda x: f"{icons[x]} {x}",  # Add icon to the option label
    index=0  # Set default to Home
)

# Display content based on menu selection
if menu == 'Home':
    home.display_home()
elif menu == 'Team Report':
    team_report.display_team_report(start_date=start_date, end_date=end_date)  # Pass start and end dates separately
elif menu == 'Player Report':
    player_report.display_player_report(player_name=player_name, start_date=start_date, end_date=end_date)  # Pass start and end dates separately
elif menu == 'Injury Prediction':
    injury_prediction.display_injury_prediction()
elif menu == 'Personalized Plan':
    personalized_plan.display_personalized_plan()


# Sidebar active state styling
if menu == 'Home':
    st.sidebar.markdown("<style>.stSelected {background-color: #DFF0FF;}</style>", unsafe_allow_html=True)
elif menu == 'Team Report':
    st.sidebar.markdown("<style>.stSelected {background-color: #DFF0FF;}</style>", unsafe_allow_html=True)
elif menu == 'Player Report':
    st.sidebar.markdown("<style>.stSelected {background-color: #DFF0FF;}</style>", unsafe_allow_html=True)
elif menu == 'Injury Prediction':
    st.sidebar.markdown("<style>.stSelected {background-color: #DFF0FF;}</style>", unsafe_allow_html=True)
elif menu == 'Personalized Plan':
    st.sidebar.markdown("<style>.stSelected {background-color: #DFF0FF;}</style>", unsafe_allow_html=True)

# Sidebar: Player Name and Date Range
with st.sidebar:
    
    # Player Name Filter
    player_name = st.selectbox("Select Player", roster_df['Player Name'].unique())

    # Date Range Filter
    st.subheader("Select Date Range")
    min_date = gps_df['Session Date'].min()
    max_date = gps_df['Session Date'].max()
    selected_date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Extract start and end dates from the range
start_date, end_date = selected_date_range