import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from .generate_pdf import generate_pdf

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to calculate BMI
def calculate_bmi(weight, height):
    if weight > 0 and height > 0:
        return weight / (height / 100) ** 2  # Convert height from cm to meters
    return 0

# Main app function
def display_personalized_plan():
    st.markdown(
        """
        <style>
        .report-title {
            font-size: 40px;
            font-weight: bold;
            color: #373433ff;
            text-align: center;
            padding-bottom: 10px;
        }
        .section-title {
            font-size: 22px;
            font-weight: bold;
            color: #444;
            margin-top: 20px;
            padding-bottom: 5px;
            background-color: #f0f0f0;
            padding-left: 10px;
        }
        .subtext {
            font-size: 14px;
            color: gray;
        }
        .plan-content {
            font-size: 16px;
            color: #333;
            line-height: 1.5;
        }
        </style>
        <div class="report-title">⚽ Dubai Club Player Personalization Tool ⚽</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="subtext">Fill out the form below to get your personalized training, recovery, and diet plan.</p>', unsafe_allow_html=True)

    # ---- Player Physical Data ----
    st.markdown('<div class="section-title">📊 Player Physical Data</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=75)
    with col2:
        height = st.number_input('Height (cm)', min_value=100, max_value=250, value=175)

    bmi = calculate_bmi(weight, height)
    st.success(f'✅ BMI: **{bmi:.2f}**')

    # ---- Performance Data ----
    st.markdown('<div class="section-title">📈 Performance Metrics</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        energy = st.slider('⚡ Energy Level', 1, 10, 5)
        stress = st.slider('😣 Stress Level', 1, 10, 5)
    with col4:
        sleep_quality = st.slider('💤 Sleep Quality', 1, 10, 5)
        soreness = st.slider('💪 Soreness Level', 1, 10, 5)

    # ---- Session & Sprint Data ----
    st.markdown('<div class="section-title">🏃 Session & Sprint Data</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        total_distance = st.number_input('Total Distance (km)', min_value=0.0, format="%.2f", value=5.0)
        minutes_per_session = st.number_input('Minutes per Session', min_value=0, max_value=300, value=60)
    with col6:
        high_speed_running = st.number_input('High-Speed Running (km)', min_value=0.0, format="%.2f", value=1.0)
        num_sprints = st.number_input('Number of Sprints', min_value=0, max_value=50, value=5)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Generate Button ----
    if st.button('🚀 Generate Personalized Plan', use_container_width=True):
        # Basic validation
        if weight <= 0 or height <= 0:
            st.error("Please enter valid weight and height values greater than zero.")
            return

        with st.spinner('🧠 Generating your optimized plan...'):
            player_data = {
                "energy": energy,
                "sleep_quality": sleep_quality,
                "stress": stress,
                "soreness": soreness,
                "total_distance": total_distance,
                "high_speed_running": high_speed_running,
                "minutes_per_session": minutes_per_session,
                "num_sprints": num_sprints,
                "weight": weight,
                "height": height,
                "bmi": bmi
            }

            system_prompt = (
                "You are a performance optimization expert specializing in football. "
                "You provide detailed, structured, and personalized training, recovery, and diet strategies "
                "based on each player's physical and performance data. "
                "Always respond in markdown format using clear headings and bullet points."
            )

            user_prompt = f"""
            📌 **Instruction**:

            1. Start with a section titled `🔍 Player Data Interpretation` presenting clear, concise bullet points that explain each physical and performance metric. Use precise, supportive language that helps the athlete understand implications for health, recovery, and elite-level performance optimization.

            2. Then create a fully customized, data-driven plan divided into three sections:
            - `🏋️ Training Plan`
            - `🛌 Recovery Plan`
            - `🍽️ Diet Plan`

            Each section must:
            - Use bullet points for clarity.
            - Employ a professional, motivating, and scientifically grounded tone.
            - Tailor recommendations precisely to the player's data and performance profile.
            - In the `🍽️ Diet Plan`, provide specific, exact food items and portion guidance to meet the athlete’s caloric and macronutrient needs, optimizing for performance, recovery, and body composition goals.

            ---

            ### 🔍 Real Player Data:
            - Weight: {weight} kg  
            - Height: {height} cm  
            - Energy Level: {energy}  
            - Stress Level: {stress}  
            - Sleep Quality: {sleep_quality}  
            - Soreness Level: {soreness}  
            - Total Distance: {total_distance} km  
            - High-Speed Running: {high_speed_running} km  
            - Minutes per Session: {minutes_per_session}  
            - Number of Sprints: {num_sprints}  
            - BMI: {bmi}  

            ---

            📌 **Guidelines**:
            - Begin with `🔍 Player Data Interpretation` in bullet points.  
            - Follow with fully tailored `🏋️ Training Plan`, `🛌 Recovery Plan`, and `🍽️ Diet Plan` sections.  
            - Use clear, professional, motivating language suited for elite athletes and coaches.  
            - Provide exact foods, portions, and meal timing in the diet plan, adjusted to the player’s profile.  
            - Avoid generic advice; every recommendation must be data-driven and specific.

            ***Generate the detailed, precise interpretation and plan now.***
            """

            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    stream=True
                )
            except Exception as e:
                st.error(f"Error generating plan: {e}")
                return

            response = ""
            placeholder = st.empty()
            for chunk in stream:
                response += chunk.choices[0].delta.content or ''
                placeholder.markdown(response)

            # PDF download button
            pdf_buffer = generate_pdf(response)
            st.download_button(
                label="📄 Download Plan as PDF",
                data=pdf_buffer,
                file_name="personalized_plan.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    display_personalized_plan()
