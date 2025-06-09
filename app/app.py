import streamlit as st
st.set_page_config(layout="wide")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PIL import Image
import home
from modules.reporting import display_team_report,display_player_report
from modules.predictions import display_injury_prediction
from modules.personalization import display_personalized_plan
import pandas as pd

# Load logo
logo = Image.open('Images/Logo.png')

# Load data
calendar_df = pd.read_csv('data/calendar_preprocessed.csv')

gps_df = pd.read_csv('data/gps_data_preprocessed.csv')
gps_df['Session Date'] = pd.to_datetime(gps_df['Session Date'], dayfirst=True, errors='coerce')
gps_df['High Speed Running'] = gps_df['Distance Zone 5'] + gps_df['Distance Zone 6']

wellness_df = pd.read_csv('data/wellness_preprocessed.csv')
wellness_df['Session Date'] = pd.to_datetime(wellness_df['Session Date'])

roster_df = pd.read_csv('data/roster_preprocessed.csv')

# Custom CSS
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #00529B;
        text-align: center;
        padding-top: 20px;
    }
    .sidebar .stSelected {
        background-color: #DFF0FF;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="title">Dubai Club For People Of Determination</div>', unsafe_allow_html=True)
st.sidebar.image(logo, use_container_width=True)

# Sidebar: Navigation menu
icons = {
    'Home': '🏠',
    'Team Report': '👥',
    'Player Report': '⚽',
    'Injury Prediction': '🤕',
    'Personalized Plan': '📝',
}
menu = st.sidebar.selectbox(
    'Choose an option:',
    ('Home', 'Team Report', 'Player Report', 'Injury Prediction', 'Personalized Plan'),
    format_func=lambda x: f"{icons[x]} {x}"
)

# Sidebar: Show filters only for Team Report and Player Report
start_date = end_date = player_name = None
if menu in ['Team Report', 'Player Report']:
    st.sidebar.subheader("Select Date Range")
    min_date = gps_df['Session Date'].min().date()
    max_date = gps_df['Session Date'].max().date()
    default_range = [min_date, max_date]

    selected_date_range = st.sidebar.date_input(
        "Date Range",
        value=default_range,
        min_value=min_date,
        max_value=max_date
    )

    start_date, end_date = selected_date_range
  

    player_name = st.sidebar.selectbox("Select Player", roster_df['Player Name'].unique(), key="select_player")

# Route to pages
if menu == 'Home':
    home.display_home()
elif menu == 'Team Report':
    if start_date and end_date:
        display_team_report(player_name, start_date, end_date, gps_df, wellness_df, roster_df)
elif menu == 'Player Report':
    if start_date and end_date:
        display_player_report(player_name, start_date, end_date, gps_df, wellness_df, roster_df)
elif menu == 'Injury Prediction':
    display_injury_prediction()
elif menu == 'Personalized Plan':
    display_personalized_plan()
