import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards

# Set the Streamlit page config as the first command in the script
st.set_page_config(page_title="Player Performance Report", page_icon="📊", layout="wide")

# Load data and cache it for performance
@st.cache_data
def load_data():
    calendar_df = pd.read_csv('data/calendar_preprocessed.csv')  # Adjust path as needed
    gps_df = pd.read_csv('data/gps_data_preprocessed.csv')  # Adjust path as needed
    wellness_df = pd.read_csv('data/wellness_preprocessed.csv')  # Adjust path as needed
    roster_df = pd.read_csv('data/roster_preprocessed.csv')  # Adjust path as needed
    
    # Calculate the metrics (HSR)
    gps_df['High Speed Running'] = gps_df['Distance Zone 5'] + gps_df['Distance Zone 6']
    
    return calendar_df, gps_df, wellness_df, roster_df

calendar_df, gps_df, wellness_df, roster_df = load_data()

# Streamlit UI Components
def display_injury_prediction():
    st.title('Player Performance Report')
