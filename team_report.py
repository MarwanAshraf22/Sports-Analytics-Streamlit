import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

def display_team_report():
    # Load data
    calendar_df = pd.read_csv('data/calendar_preprocessed.csv')
    gps_df = pd.read_csv('data/gps_data_preprocessed.csv')
    wellness_df = pd.read_csv('data/wellness_preprocessed.csv')
    roster_df = pd.read_csv('data/roster_preprocessed.csv')
    
    gps_df['Session Date'] = pd.to_datetime(gps_df['Session Date']).dt.date
    wellness_df['Session Date'] = pd.to_datetime(wellness_df['Session Date'])

    # Merge gps_df with roster_df to get the Position data
    filtered_gps = pd.merge(gps_df, roster_df[['Player Name', 'Position']], on='Player Name', how='left')

    # Streamlit UI Components
    st.markdown(
        """
        <style>
        .report-title {
            font-size: 36px;
            font-weight: bold;
            color: #506B77ff;  /* Real Madrid Blue */
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        <div class="report-title">
           ⚽ Team Performance Report ⚽
        </div>
        """, unsafe_allow_html=True)

    # Date Range Selection
    min_date = gps_df['Session Date'].min()
    max_date = gps_df['Session Date'].max()
    selected_date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date, key="team_date_range")
    
    # Filter gps_df based on the selected date range
    filtered_gps = filtered_gps[(filtered_gps['Session Date'] >= selected_date_range[0]) & (filtered_gps['Session Date'] <= selected_date_range[1])]
    
    # Drill name filter: Only keep specific drills
    drill_names_to_include = ['Entire Session', 'SSG 5v5', 'Possession Drill', 'Warm Up', 'Finishing Drill']
    filtered_gps = filtered_gps[filtered_gps['Drill Name'].isin(drill_names_to_include)]

    # Section 1: Total Session Stats with Metric Cards
    st.header("Session Stats")
    total_distance_card = filtered_gps['Total Distance'].sum()
    avg_speed = filtered_gps['Metres Per Minute'].mean()
    max_speed = filtered_gps['Maximum Speed'].max()
    rpe = ((max_speed + avg_speed / 1000) * 0.1) + 2  # Estimate RPE
    hsr = avg_speed  # High-Speed Running (average speed)

    # Metric data for displaying in cards
    metric_data = [
        {"label": "Total Distance", "value": f"{total_distance_card:.2f} meters", "delta": 0},
        {"label": "RPE", "value": f"{rpe:.2f}", "delta": 0},
        {"label": "HSR (Avg Speed)", "value": f"{hsr:.2f} m/s", "delta": 0},
    ]

    # Apply the style to metric cards with custom colors
    style_metric_cards(
        background_color="#E3F2FD",  # Light blue background
        border_size_px=3,  # Border size
        border_color="#0288D1",  # Blue border color
        border_radius_px=12,  # Rounded corners
        border_left_color="#81D4FA",  # Light cyan left border
        box_shadow=True  # Apply box shadow
    )  # Styling the metric cards

    # Display the metrics in cards using the metric_cards function
    col1, col2, col3 = st.columns(3)  # Using three columns for displaying the metrics side by side
    with col1:
        st.metric(label=metric_data[0]['label'], value=metric_data[0]['value'], delta=metric_data[0]['delta'])
    with col2:
        st.metric(label=metric_data[1]['label'], value=metric_data[1]['value'], delta=metric_data[1]['delta'])
    with col3:
        st.metric(label=metric_data[2]['label'], value=metric_data[2]['value'], delta=metric_data[2]['delta'])

    # Section 2: Player-Level Data with Additional Metrics
    st.header("Player Performance Data")
    player_data = filtered_gps.groupby('Player Name').agg({
        'Total Distance': 'sum', 
        'Maximum Speed': 'max',
        'Metres Per Minute': 'mean',
        'Explosive Distance': 'sum',
        'Session Time(mins)': 'sum'
    }).reset_index()

    # Add new KPIs
    player_data['% MAX TD'] = (player_data['Total Distance'] / total_distance_card) * 100
    player_data['% MAX HSR'] = (player_data['Metres Per Minute'] / max_speed) * 100
    player_data['% MAX SPD'] = (player_data['Maximum Speed'] / max_speed) * 100

    # Display the player data table with KPIs
    st.dataframe(player_data)

    # Section 3: Drill-Specific Stats and Player Comparison Combined
    st.header("Drill-Specific Stats and Player Comparison")
    drill_distribution = filtered_gps.groupby('Drill Name').agg({
        'Total Distance': 'sum', 
        'Metres Per Minute': 'mean',
        'Maximum Speed': 'max'
    }).reset_index()

    # Bar chart for distance covered in each drill
    fig_drill = px.bar(drill_distribution, x='Drill Name', y='Total Distance', color='Drill Name', title="Distance Covered in Each Drill", color_discrete_sequence=["#0288D1", "#FF8A65", "#C5E1A5", "#8E24AA", "#FBC02D"])
    
    # Player comparison: Total Distance vs Speed
    fig_comparison = px.bar(player_data, x='Player Name', y=['Total Distance', 'Maximum Speed'], barmode='group', title="Player Comparison: Total Distance vs Speed")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_drill)
    with col2:
        st.plotly_chart(fig_comparison)

    # Section 4: Position & Drill Comparison (Avg Distance by Position and Drill)
    st.header("Avg Total Distance by Position & Drill")
    position_drill_data = filtered_gps.groupby(['Position', 'Drill Name']).agg({'Total Distance': 'mean'}).reset_index()

    # Bar chart for avg distance by position and drill
    fig_position_drill = px.bar(position_drill_data, x='Position', y='Total Distance', color='Drill Name', barmode='group', title="Avg Total Distance by Position & Drill")
    st.plotly_chart(fig_position_drill)

    # Section 5: % Game TD & HSR Comparison
    st.header("Player Performance vs Max Game (TD & HSR)")
    game_performance = player_data[['Player Name', '% MAX TD', '% MAX HSR']]
    fig_game_comparison = px.bar(game_performance, x='Player Name', y=['% MAX TD', '% MAX HSR'], barmode='group', title="% Game TD & HSR Comparison")
    st.plotly_chart(fig_game_comparison)

    # Section 6: Heatmap - Player Speed vs Distance across Drills and Scatter Plot Combined
    st.header("Speed vs Distance: Heatmap & Scatter Plot")
    drill_speed_distance = filtered_gps.groupby(['Player Name', 'Drill Name']).agg({
        'Metres Per Minute': 'mean',
        'Total Distance': 'sum'
    }).reset_index()

    heatmap_data = drill_speed_distance.pivot(index='Player Name', columns='Drill Name', values='Total Distance')
    fig_heatmap = px.imshow(heatmap_data, title="Heatmap: Player's Speed and Distance Across Drills", labels=dict(x="Drill Name", y="Player Name"))

    fig_scatter = px.scatter(filtered_gps, x='Metres Per Minute', y='Total Distance', color='Drill Name', title="Speed vs Distance")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_heatmap)
    with col2:
        st.plotly_chart(fig_scatter)

    # Section 7: Donut Chart and Total Distance vs Max Speed Combined
    st.header("Total Distance vs Max Speed & Drill Distribution")
    drill_distance = filtered_gps.groupby('Drill Name').agg({'Total Distance': 'sum'}).reset_index()
    fig_donut = go.Figure(data=[go.Pie(labels=drill_distance['Drill Name'], values=drill_distance['Total Distance'], hole=0.4, marker=dict(colors=["#FF5722", "#FBC02D", "#0288D1"]))])
    fig_donut.update_layout(title="Total Distance Covered by Each Drill")

    fig_total_vs_speed = px.scatter(player_data, x='Total Distance', y='Maximum Speed', color='Player Name', title="Total Distance vs Max Speed")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut)
    with col2:
        st.plotly_chart(fig_total_vs_speed)

    # Section 10: KPI Distribution per Player (Box Plot)
    st.header("KPI Distribution per Player")
    fig_kpi_distribution = px.box(filtered_gps, x='Player Name', y='Total Distance', title="KPI Distribution: Total Distance by Player")
    st.plotly_chart(fig_kpi_distribution)

    # Section 15: Session Time vs Distance (Bubble Chart)
    st.header("Session Time vs Distance & Speed")
    fig_bubble = px.scatter(filtered_gps, x='Total Distance', y='Metres Per Minute', size='Session Time(mins)', color='Drill Name', title="Session Time vs Distance & Speed")
    st.plotly_chart(fig_bubble)

display_team_report()
