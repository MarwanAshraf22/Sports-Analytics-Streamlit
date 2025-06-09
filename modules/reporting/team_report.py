import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

def display_team_report(player_name, start_date, end_date, gps_df, wellness_df, roster_df):
    # Define custom color palette from the logo
    custom_colors = ['#003366', '#0072C6', '#81D4FA', '#FFD700']

    st.markdown(
        """
        <style>
        body {
            font-family: 'Dubai', sans-serif;
        }
        .report-title {
            font-size: 36px;
            font-weight: bold;
            color: #003366;
            text-align: center;
            background-color: #D6EFFF;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
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
        }
        .player-info p {
            font-size: 18px;
            margin: 2px 0;
        }
        </style>

        <div class="report-title">📊 Team Report 📊</div>
        """, unsafe_allow_html=True)

    gps_df['Session Date'] = pd.to_datetime(gps_df['Session Date']).dt.date
    wellness_df['Session Date'] = pd.to_datetime(wellness_df['Session Date']).dt.date

    filtered_gps = pd.merge(gps_df, roster_df[['Player Name', 'Position']], on='Player Name', how='left')
    filtered_gps = filtered_gps[(filtered_gps['Session Date'] >= start_date) & (filtered_gps['Session Date'] <= end_date)]

    st.header("Session Stats")
    total_distance_card = (filtered_gps['Total Distance'].sum()) / 1000
    avg_speed = filtered_gps['Metres Per Minute'].mean()
    max_speed = filtered_gps['Maximum Speed'].max()
    rpe = ((max_speed + avg_speed / 1000) * 0.1) + 2
    hsr = avg_speed

    metric_data = [
        {"label": "Total Distance", "value": f"{total_distance_card:.2f} km"},
        {"label": "RPE", "value": f"{rpe:.2f}"},
        {"label": "HSR (Avg Speed)", "value": f"{hsr:.2f} m/s"},
    ]

    style_metric_cards(
        background_color="#E6F4FF",
        border_size_px=3,
        border_color="#0072C6",
        border_radius_px=12,
        border_left_color="#81D4FA",
        box_shadow=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=metric_data[0]['label'], value=metric_data[0]['value'])
    with col2:
        st.metric(label=metric_data[1]['label'], value=metric_data[1]['value'])
    with col3:
        st.metric(label=metric_data[2]['label'], value=metric_data[2]['value'])

    st.header("Player Performance Data")
    player_data = filtered_gps.groupby('Player Name').agg({
        'Total Distance': 'sum', 
        'Maximum Speed': 'max',
        'Metres Per Minute': 'mean',
        'Explosive Distance': 'sum',
        'Session Time(mins)': 'sum'
    }).reset_index()

    player_data['% MAX TD'] = (player_data['Total Distance'] / total_distance_card) * 100
    player_data['% MAX HSR'] = (player_data['Metres Per Minute'] / max_speed) * 100
    player_data['% MAX SPD'] = (player_data['Maximum Speed'] / max_speed) * 100
    st.dataframe(player_data)

    st.header("Drill-Specific Stats and Player Comparison")
    drill_distribution = filtered_gps.groupby('Drill Name').agg({
        'Total Distance': 'sum', 
        'Metres Per Minute': 'mean',
        'Maximum Speed': 'max'
    }).reset_index()

    fig_drill = px.bar(drill_distribution, x='Drill Name', y='Total Distance', color='Drill Name',
                       title="Distance Covered in Each Drill", color_discrete_sequence=custom_colors)

    fig_comparison = px.bar(player_data, x='Player Name', y=['Total Distance', 'Maximum Speed'], barmode='group',
                            title="Player Comparison: Total Distance vs Speed", color_discrete_sequence=custom_colors)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_drill, key="drill_chart")
    with col2:
        st.plotly_chart(fig_comparison, key="comparison_chart")

    st.header("Avg Total Distance by Position & Drill")
    position_drill_data = filtered_gps.groupby(['Position', 'Drill Name']).agg({'Total Distance': 'mean'}).reset_index()
    fig_position_drill = px.bar(position_drill_data, x='Position', y='Total Distance', color='Drill Name',
                                barmode='group', color_discrete_sequence=custom_colors)
    st.plotly_chart(fig_position_drill, key="position_drill_chart")

    st.header("Player Performance vs Max Game (TD & HSR)")
    game_performance = player_data[['Player Name', '% MAX TD', '% MAX HSR']]
    fig_game_comparison = px.bar(game_performance, x='Player Name', y=['% MAX TD', '% MAX HSR'],
                                 barmode='group', title="% Game TD & HSR Comparison",
                                 color_discrete_sequence=custom_colors)
    st.plotly_chart(fig_game_comparison, key="game_comparison_chart")

    st.header("Speed vs Distance: Heatmap & Scatter Plot")
    drill_speed_distance = filtered_gps.groupby(['Player Name', 'Drill Name']).agg({
        'Metres Per Minute': 'mean',
        'Total Distance': 'sum'
    }).reset_index()

    heatmap_data = drill_speed_distance.pivot(index='Player Name', columns='Drill Name', values='Total Distance')
    fig_heatmap = px.imshow(heatmap_data, title="Heatmap: Player's Speed and Distance Across Drills",
                            labels=dict(x="Drill Name", y="Player Name"),
                            color_continuous_scale=custom_colors)

    fig_scatter = px.scatter(filtered_gps, x='Metres Per Minute', y='Total Distance', color='Drill Name',
                             title="Speed vs Distance", color_discrete_sequence=custom_colors)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_heatmap, key="heatmap_chart")
    with col2:
        st.plotly_chart(fig_scatter, key="scatter_chart")

    st.header("Total Distance vs Max Speed & Drill Distribution")
    drill_distance = filtered_gps.groupby('Drill Name').agg({'Total Distance': 'sum'}).reset_index()
    fig_donut = go.Figure(data=[go.Pie(labels=drill_distance['Drill Name'], values=drill_distance['Total Distance'],
                                       hole=0.4)])
    fig_donut.update_traces(marker=dict(colors=custom_colors))
    fig_donut.update_layout(title="Total Distance Covered by Each Drill")

    fig_total_vs_speed = px.scatter(player_data, x='Total Distance', y='Maximum Speed', color='Player Name',
                                    title="Total Distance vs Max Speed", color_discrete_sequence=custom_colors)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, key="donut_chart")
    with col2:
        st.plotly_chart(fig_total_vs_speed, key="total_vs_speed_chart")

    st.header("KPI Distribution per Player")
    fig_kpi_distribution = px.box(filtered_gps, x='Player Name', y='Total Distance',
                                  title="Distribution of Total Distance per Player",
                                  color_discrete_sequence=custom_colors)
    st.plotly_chart(fig_kpi_distribution, key="kpi_distribution_chart")

    st.header("Session Time vs Distance & Speed")
    fig_bubble = px.scatter(filtered_gps, x='Total Distance', y='Metres Per Minute',
                            size='Session Time(mins)', color='Drill Name',
                            title="Session Time vs Distance & Speed",
                            color_discrete_sequence=custom_colors)
    st.plotly_chart(fig_bubble, key="bubble_chart")
