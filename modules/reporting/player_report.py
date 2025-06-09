import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards

def display_player_report(player_name, start_date, end_date, gps_df, wellness_df, roster_df):
    # Define custom color palette
    custom_colors = ['#003366', '#0072C6', '#81D4FA', '#FFD700']

    st.markdown(
        """
        <style>
        .report-title {
            font-size: 36px;
            font-weight: bold;
            color: #003366;
            text-align: center;
            background-color: #D6EFFF;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
            font-family: 'Dubai', sans-serif;
        }
        .player-info {
            background-color: #D6EFFF;
            padding: 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            color: #003366;
        }
        .player-info h3 {
            font-size: 26px;
            margin-bottom: 5px;
            font-family: 'Dubai', sans-serif;
        }
        .player-info p {
            font-size: 18px;
            margin: 2px 0;
            font-family: 'Dubai', sans-serif;
        }
        </style>

        <div class="report-title">📝 Player Performance Report 📝</div>
        """,
        unsafe_allow_html=True
    )

    # Filter by player and date range
    filtered_gps_data = gps_df[(pd.to_datetime(gps_df['Session Date']) >= pd.to_datetime(start_date)) &
                               (pd.to_datetime(gps_df['Session Date']) <= pd.to_datetime(end_date))]
    filtered_wellness_data = wellness_df[(pd.to_datetime(wellness_df['Session Date']) >= pd.to_datetime(start_date)) &
                                         (pd.to_datetime(wellness_df['Session Date']) <= pd.to_datetime(end_date))]

    player_gps_data = filtered_gps_data[filtered_gps_data['Player Name'] == player_name].copy()
    player_wellness_data = filtered_wellness_data[filtered_wellness_data['Player Name'] == player_name].copy()

    if player_gps_data.empty or player_wellness_data.empty:
        st.warning("No data available for this player in the selected date range.")
        return

    player_gps_data['Session Display'] = pd.to_datetime(player_gps_data['Session Date']).dt.strftime('%d-%m-%Y')
    player_wellness_data['Session Display'] = pd.to_datetime(player_wellness_data['Session Date']).dt.strftime('%d-%m-%Y')

    player_gps_data.sort_values('Session Display', inplace=True)
    player_wellness_data.sort_values('Session Display', inplace=True)

    player_roster_data = roster_df[roster_df['Player Name'] == player_name]
    if player_roster_data.empty:
        st.error("Player not found in roster.")
        return

    player_roster = player_roster_data.iloc[0]
    birth_date = pd.to_datetime(player_roster['DOB'])
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Player Card
    st.markdown(f'''
    <div class="player-info">
        <img src="{player_roster['Player Image']}" width="140" style="border-radius: 50%;" />
        <div style="margin-left: 20px;">
            <h3>{player_name}</h3>
            <p>Position: {player_roster['Position']}</p>
            <p>Age: {age} years old</p>
            <img src="{player_roster['International Image']}" width="50" style="margin-top: 10px;" />
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Metric Cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric("High Speed Running", f"{player_gps_data['High Speed Running'].mean():.2f} m")
    with col2:
        avg_wellness_score = player_wellness_data['Total Score'].mean()
        st.metric("Average Wellness Score", f"{avg_wellness_score:.2f}")

    style_metric_cards(
        background_color="#E6F4FF",
        border_size_px=3,
        border_color="#0072C6",
        border_radius_px=12,
        border_left_color="#81D4FA",
        box_shadow=True
    )

    # Data Tables
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Performance Metrics")
        st.write(player_gps_data[['Session Display', 'Total Distance', 'High Speed Running', 'Session Time(mins)']])
    with col2:
        st.subheader("Wellness Metrics")
        st.write(player_wellness_data[['Session Display', 'Energy', 'Sleep Quality', 'Stress', 'Soreness', 'Total Score']])

    # Performance Ratios
    total_high_speed_running = player_gps_data['High Speed Running'].sum()
    total_distance = player_gps_data['Total Distance'].sum()
    max_game_high_speed_running = player_roster['Max Game High Speed Running']
    max_game_total_distance = player_roster['Max Game Total Distance']
    daily_max_hsr = player_gps_data['High Speed Running'].max()
    daily_max_td = player_gps_data['Total Distance'].max()

    max_game_hsr = (total_high_speed_running / max_game_high_speed_running) * 100 if max_game_high_speed_running else 0
    max_game_td = (total_distance / max_game_total_distance) * 100 if max_game_total_distance else 0
    max_td = (total_distance / daily_max_td) * 100 if daily_max_td else 0
    max_hsr = (total_high_speed_running / daily_max_hsr) * 100 if daily_max_hsr else 0

    # Performance Bar Chart
    st.subheader("Performance Metrics Comparison")
    performance_data = {
        "Metric": ["% MAX Game HSR", "% MAX Game TD", "% MAX TD", "% MAX HSR"],
        player_name: [max_game_hsr, max_game_td, max_td, max_hsr]
    }
    performance_df = pd.DataFrame(performance_data)

    fig = px.bar(performance_df, x='Metric', y=player_name,
                 title='Performance Metrics Comparison',
                 color_discrete_sequence=[custom_colors[1]],
                 text_auto='.2f')
    fig.update_layout(yaxis_tickformat='%')
    st.plotly_chart(fig)

    # Charts: HSR and Energy Z-Score
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(player_gps_data, x='Session Display', y='High Speed Running',
                         title=f'High Speed Running vs Session Date for {player_name}',
                         labels={'Session Display': 'Date', 'High Speed Running': 'High Speed Running (m)'},
                         color='High Speed Running',
                         color_continuous_scale=custom_colors)
        st.plotly_chart(fig)

    with col2:
        wellness_scores = player_wellness_data[['Session Display', 'Energy']].copy()
        wellness_scores['Z-Score Energy'] = stats.zscore(wellness_scores['Energy'])
        fig4 = px.line(wellness_scores, x='Session Display', y='Z-Score Energy',
                       title=f'Energy Z-Score for {player_name}',
                       line_shape='linear',
                       markers=True,
                       color_discrete_sequence=[custom_colors[1]])
        st.plotly_chart(fig4)
