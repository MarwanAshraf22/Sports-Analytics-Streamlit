import streamlit as st
import joblib
import numpy as np
import os 

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'injury_risk_model.pkl'))
model = joblib.load(model_path)

# Function to display the injury prediction UI
def display_injury_prediction():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Dubai', sans-serif;
        }
        .injury-title {
            font-size: 36px;
            font-weight: bold;
            color: #003366;
            background-color: #D6EFFF;
            text-align: center;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 25px;
            font-family: 'Dubai', sans-serif;
        }
        .section-header {
            font-size: 20px;
            font-weight: 600;
            color: #003366;
            background-color: #D6EFFF;
            padding: 10px 15px;
            border-radius: 8px;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        </style>
        <div class="injury-title">🚑 Injury Risk Prediction 🚑</div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        total_distance = st.number_input(
            "🏃 Total Distance (meters)", min_value=0.0, format="%.2f",
            help="Total distance run in meters during the session."
        )
        metres_per_minute = st.number_input(
            "⏱️ Metres Per Minute", min_value=0.0, format="%.2f",
            help="Average running speed in meters per minute."
        )
        high_speed_running = st.number_input(
            "⚡ High-Speed Running (meters)", min_value=0.0, format="%.2f",
            help="Distance covered at high intensity (e.g., sprinting)."
        )

    with col2:
        energy = st.slider(
            "🔋 Energy Level", min_value=0, max_value=10, value=5,
            help="Energy level on a scale from 0 (low) to 10 (high)."
        )
        soreness = st.slider(
            "💢 Soreness Level", min_value=0, max_value=10, value=5,
            help="Muscle soreness level from 0 (none) to 10 (severe)."
        )
        stress = st.slider(
            "😓 Stress Level", min_value=0, max_value=10, value=5,
            help="Mental/physical stress level from 0 (low) to 10 (high)."
        )

    st.markdown("---")

    # Prediction
    if st.button('🚑 Predict Injury Risk', use_container_width=True):
        with st.spinner("Analyzing injury risk..."):
            if total_distance < 0 or metres_per_minute < 0 or high_speed_running < 0:
                st.error("⚠️ Please ensure that all input values are non-negative.")
            else:
                features = np.array([[total_distance, metres_per_minute, high_speed_running,
                                      energy, soreness, stress]])
                prediction = model.predict(features)

                if prediction == 1:
                    st.error("🔥 **High Injury Risk!** Reduce intensity and prioritize recovery.")
                else:
                    st.success("✅ **Low Injury Risk!** Keep up the great work.")
