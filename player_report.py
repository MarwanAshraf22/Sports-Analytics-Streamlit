import streamlit as st

def display_player_report():
    st.markdown('<div class="subheader">Player Report</div>', unsafe_allow_html=True)
    st.write("""
    The player report section will provide detailed insights about individual players, such as their career achievements, stats, and more.
    """)
