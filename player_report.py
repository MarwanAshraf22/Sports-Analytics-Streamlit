import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards


# Load data and cache it for performance
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
def display_player_report():

    # Streamlit Header with Custom Styling
    st.markdown(
        """
        <style>
        .report-title {
            font-size: 36px;
            font-weight: bold;
            color: #0288D1;  /* Real Madrid Blue */
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        <div class="report-title">
        📝 Player Performance Report 📝
        </div>
        """, unsafe_allow_html=True)

    # Player Name Filter on the Main Page
    player_name = st.selectbox("Select Player", roster_df['Player Name'].unique(),key="player_name_selectbox_unique")

    # Date Range Filter on the Main Page
    st.subheader("Select Date Range")
    start_date = st.date_input("Start Date", 
                           min_value=min(gps_df['Session Date']), 
                           max_value=max(gps_df['Session Date']), 
                           value=min(gps_df['Session Date']),
                           key="start_date_input_unique")

    end_date = st.date_input("End Date", 
                            min_value=min(gps_df['Session Date']), 
                            max_value=max(gps_df['Session Date']), 
                            value=max(gps_df['Session Date']),
                            key="end_date_input_unique")

    # Convert the dates to the correct format for filtering
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the data based on the selected date range and player
    filtered_gps_data = gps_df[(pd.to_datetime(gps_df['Session Date']) >= start_date) & (pd.to_datetime(gps_df['Session Date']) <= end_date)]
    filtered_wellness_data = wellness_df[(pd.to_datetime(wellness_df['Session Date']) >= start_date) & (pd.to_datetime(wellness_df['Session Date']) <= end_date)]

    # Filter data for the selected player
    player_gps_data = filtered_gps_data[filtered_gps_data['Player Name'] == player_name]
    player_wellness_data = filtered_wellness_data[filtered_wellness_data['Player Name'] == player_name]

    # Filtered Data for Player
    player_roster = roster_df[roster_df['Player Name'] == player_name].iloc[0]

    # Calculate the player's age based on DOB
    birth_date = pd.to_datetime(player_roster['DOB'])
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Display player details in a card-like format
    st.markdown(f'''
    <div style="background-color: #F4F4F4; padding: 20px; border-radius: 10px; display: flex; align-items: center;">
        <img src="{player_roster['Player Image']}" width="150" style="border-radius: 50%;" />
        <div style="margin-left: 20px;">
            <h3 style="font-family: 'Arial', sans-serif; font-size: 28px;">{player_name}</h3>
            <p style="font-family: 'Verdana', sans-serif; font-size: 20px; margin: 0;">Position: {player_roster['Position']}</p>
            <p style="font-family: 'Verdana', sans-serif; font-size: 20px; margin: 0;">Age: {age} years old</p>
            <img src="{player_roster['International Image']}" width="50" style="margin-top: 10px;" />
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Apply the card styling for key performance metrics
    style_metric_cards(
        background_color="#E3F2FD",  # Light blue background
        border_size_px=3,  # Border size
        border_color="#0288D1",  # Blue border color
        border_radius_px=12,  # Rounded corners
        border_left_color="#81D4FA",  # Light cyan left border
        box_shadow=True  # Apply box shadow
    )

    # Create cards for key performance metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("High Speed Running", f"{player_gps_data['High Speed Running'].mean():.2f} m", delta=None)
    with col2:
        avg_wellness_score = player_wellness_data['Total Score'].mean()
        st.metric("Average Wellness Score", f"{avg_wellness_score:.2f}", delta=None)

    # Display performance metrics (Total Distance, Session Time, etc.)
    st.subheader("Performance Metrics")
    st.write(player_gps_data[['Session Date', 'Total Distance', 'High Speed Running', 'Session Time(mins)']])

    # Calculate performance metrics
    total_high_speed_running = player_gps_data['High Speed Running'].sum()
    total_distance = player_gps_data['Total Distance'].sum()

    max_game_high_speed_running = player_roster['Max Game High Speed Running']
    max_game_total_distance = player_roster['Max Game Total Distance']
    
    # Calculate Daily Max HSR (similar to the DAX formula)
    daily_max_hsr = player_gps_data.groupby('Player Name')['High Speed Running'].max().loc[player_name]

    # Calculate Daily Max TD (similar to the DAX formula)
    daily_max_td = player_gps_data.groupby('Player Name')['Total Distance'].max().loc[player_name]

    # Calculate percentage metrics
    max_game_hsr = (total_high_speed_running / max_game_high_speed_running) * 100
    max_game_td = (total_distance / max_game_total_distance) * 100
    max_td = (total_distance / daily_max_td) * 100
    max_hsr = (total_high_speed_running / daily_max_hsr) * 100

    # Add the Bar Chart for Performance Metrics Comparison
    st.subheader("Performance Metrics Comparison")
    performance_data = {
        "Metric": ["% MAX Game HSR", "% MAX Game TD", "% MAX TD", "% MAX HSR"],
        "Carvajal": [max_game_hsr, max_game_td, max_td, max_hsr]
    }
    performance_df = pd.DataFrame(performance_data)

    # Create Bar Chart
    fig = px.bar(performance_df, x='Metric', y='Carvajal', title='Performance Metrics Comparison')
    st.plotly_chart(fig)

    # Create side-by-side visualizations
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(player_gps_data, x='Session Date', y='High Speed Running',
                         title=f'High Speed Running vs Session Time for {player_name}',
                         labels={'Session Date': 'Date', 'High Speed Running': 'High Speed Running (m)'},
                         color='High Speed Running', color_continuous_scale='Viridis')  # Color scheme improvement
        st.plotly_chart(fig)

    with col2:
        # Create a Z-Score Wellness Plot for comparison
        wellness_scores = player_wellness_data[['Session Date', 'Energy', 'Soreness', 'Sleep Quality', 'Stress', 'Total Score']]
        wellness_scores['Z-Score Energy'] = stats.zscore(wellness_scores['Energy'])
        fig4 = px.line(wellness_scores, x='Session Date', y='Z-Score Energy', title=f'Energy Z-Score for {player_name}')
        st.plotly_chart(fig4)

    # Display wellness data (Energy, Sleep Quality, Stress, etc.)
    st.subheader("Wellness Metrics")
    st.write(player_wellness_data[['Session Date', 'Energy', 'Sleep Quality', 'Stress', 'Soreness', 'Total Score']])

# Run the player report display function
display_player_report()
