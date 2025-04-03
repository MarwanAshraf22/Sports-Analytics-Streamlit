import streamlit as st
import joblib
import numpy as np
from PIL import Image

# Load the trained model
model = joblib.load('injury_risk_model.pkl')

# Function to display the injury prediction UI
def display_injury_prediction():
    # Title with color (Real Madrid Blue), center alignment, and icon (only for this page)
    st.markdown(
        """
        <style>
        .injury-title {
            font-size: 36px;
            font-weight: bold;
            color: #B6444Aff; /* Real Madrid Blue */
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        <div class="injury-title">
           🚑 Injury Risk Prediction 🚑
        </div>
        """, unsafe_allow_html=True)
   
    # Create layout
    col1, col2 = st.columns(2)
    
    with col1:
        total_distance = st.number_input("🏃 Total Distance (meters)", min_value=0.0, format="%.2f", help="Total distance run in meters during the session.")
        metres_per_minute = st.number_input("⏱️ Metres Per Minute", min_value=0.0, format="%.2f", help="Average running speed in meters per minute.")
        high_speed_running = st.number_input("⚡ High-Speed Running (meters)", min_value=0.0, format="%.2f", help="Total distance covered in high-speed running (e.g., sprinting).")
        
    with col2:
        energy = st.slider("🔋 Energy Level", min_value=0, max_value=10, value=5, help="Current energy level on a scale from 0 (low) to 10 (high).")
        soreness = st.slider("💢 Soreness Level", min_value=0, max_value=10, value=5, help="Current soreness level on a scale from 0 (none) to 10 (severe).")
        stress = st.slider("😓 Stress Level", min_value=0, max_value=10, value=5, help="Current stress level on a scale from 0 (low) to 10 (high).")
    
    st.markdown("---")
    
    # Predict injury risk when the button is clicked
    if st.button('🚑 Predict Injury Risk', use_container_width=True):
        with st.spinner('Analyzing injury risk...'):  # Show a spinner
            # Validate input: Ensure that all values are realistic for injury prediction
            if total_distance < 0 or metres_per_minute < 0 or high_speed_running < 0:
                st.error("⚠️ Please ensure that all input values are positive.")
            else:
                # Prepare the feature array for prediction
                features = np.array([[total_distance, metres_per_minute, high_speed_running,
                                      energy, soreness, stress]])
                prediction = model.predict(features)
        
                # Display the result with colors
                if prediction == 1:
                    st.error("🔥 **High Injury Risk!** Reduce intensity and prioritize recovery.")
                else:
                    st.success("✅ **Low Injury Risk!** Keep up the great work.")

# Run the UI
display_injury_prediction()
