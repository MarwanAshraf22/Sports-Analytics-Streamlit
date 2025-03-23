import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def display_team_report():
    # Load data
    calendar_df = pd.read_csv('data/calendar_preprocessed.csv')
    gps_df = pd.read_csv('data/gps_data_preprocessed.csv')
    roster_df = pd.read_csv('data/roster_preprocessed.csv')
    wellness_df = pd.read_csv('data/wellness_preprocessed.csv')

    # Insights
    highest_speed = gps_df['Maximum Speed'].max()
    highest_speed_player = gps_df[gps_df['Maximum Speed'] == highest_speed]['Player Name'].iloc[0]

    total_distance = gps_df.groupby('Player Name')['Total Distance'].sum().reset_index()
    wellness_scores = wellness_df.groupby('Players Name')['Total Score'].mean().reset_index()
    
    total_distance_card = total_distance['Total Distance'].sum()

    activity_counts = calendar_df['Activity'].value_counts().reset_index()
    activity_counts.columns = ['Activity', 'Count']



