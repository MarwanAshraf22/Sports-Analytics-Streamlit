import streamlit as st
from PIL import Image
import home
import team_report
import player_report
import injury_prediction
import personalized_plan

# Load the logo
logo = Image.open('Images/Logo.png')

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

# Sidebar filters
with st.sidebar:
    # Player Name Filter
    player_name = st.selectbox("Select Player", player_report.roster_df['Player Name'].unique(), key="player_name_selectbox")

    # Date Range Filter
    st.subheader("Select Date Range")
    start_date = st.date_input("Start Date", 
                               min_value=min(player_report.gps_df['Session Date']), 
                               max_value=max(player_report.gps_df['Session Date']), 
                               value=min(player_report.gps_df['Session Date']),
                               key="start_date_input")

    end_date = st.date_input("End Date", 
                             min_value=min(player_report.gps_df['Session Date']), 
                             max_value=max(player_report.gps_df['Session Date']), 
                             value=max(player_report.gps_df['Session Date']),
                             key="end_date_input")

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
    team_report.display_team_report()
elif menu == 'Player Report':
    player_report.display_player_report()
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

# Add responsiveness with custom CSS for small screens
st.markdown(
    """
    <style>
    @media (max-width: 800px) {
        .title {
            font-size: 28px;
        }
        .subheader {
            font-size: 20px;
        }
        .content {
            font-size: 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Loading indicator for dynamic pages (for example, on data fetching)
def show_loading_spinner():
    with st.spinner('Loading, please wait...'):
        # Simulate a delay for loading data (e.g., fetching reports)
        import time
        time.sleep(2)

# Example of implementing the loading spinner when changing pages
if menu == 'Team Report':
    show_loading_spinner()
    team_report.display_team_report()
elif menu == 'Player Report':
    show_loading_spinner()
    player_report.display_player_report()
elif menu == 'Injury Prediction':
    show_loading_spinner()
    injury_prediction.display_injury_prediction()
elif menu == 'Personalized Plan':
    show_loading_spinner()
    personalized_plan.display_personalized_plan()
