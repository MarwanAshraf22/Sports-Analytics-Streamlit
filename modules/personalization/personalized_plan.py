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
        return weight / (height / 100) ** 2
    return 0

# Main app function
def display_personalized_plan():
    # Theme-based styling
    st.markdown(
        """
        <style>
        body {
            font-family: 'Dubai', sans-serif;
        }
        .title-box {
            background-color: #D6EFFF;
            padding: 20px;
            border-radius: 12px;
            color: #003366;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }
        .section-header {
            background-color: #D6EFFF;
            padding: 10px 15px;
            border-radius: 8px;
            margin-top: 25px;
            margin-bottom: 10px;
            color: #003366;
            font-size: 20px;
            font-weight: 600;
        }
        .response-box {
            background-color: #FFFFFF;
            color: #003366;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #cce0f4;
            margin-top: 20px;
            line-height: 1.6;
            font-size: 16px;
        }
        .response-box h3 {
            color: #004080;
            margin-top: 20px;
            font-weight: 700;
            font-size: 20px;
        }
        .response-box ul {
            margin-left: 20px;
        }
        </style>
        <div class="title-box">⚽ Dubai Club Player Personalization Tool ⚽</div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Fill out the form below to get your personalized training, recovery, and diet plan.")

    # ---- Player Physical Data ----
    st.markdown('<div class="section-header">📊 Player Physical Data</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=75)
    with col2:
        height = st.number_input('Height (cm)', min_value=100, max_value=250, value=175)

    bmi = calculate_bmi(weight, height)
    st.success(f'✅ BMI: **{bmi:.2f}**')

    # ---- Performance Data ----
    st.markdown('<div class="section-header">📈 Performance Metrics</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        energy = st.slider('⚡ Energy Level', 1, 10, 5)
        stress = st.slider('😣 Stress Level', 1, 10, 5)
    with col4:
        sleep_quality = st.slider('💤 Sleep Quality', 1, 10, 5)
        soreness = st.slider('💪 Soreness Level', 1, 10, 5)

    # ---- Session & Sprint Data ----
    st.markdown('<div class="section-header">🏃 Session & Sprint Data</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        total_distance = st.number_input('Total Distance (km)', min_value=0.0, format="%.2f", value=5.0)
        minutes_per_session = st.number_input('Minutes per Session', min_value=0, max_value=300, value=60)
    with col6:
        high_speed_running = st.number_input('High-Speed Running (km)', min_value=0.0, format="%.2f", value=1.0)
        num_sprints = st.number_input('Number of Sprints', min_value=0, max_value=50, value=5)

    st.markdown("---")

    # ---- Generate Button ----
    if st.button('🚀 Generate Personalized Plan', use_container_width=True):
        if weight <= 0 or height <= 0:
            st.error("Please enter valid weight and height values greater than zero.")
            return

        with st.spinner('🧠 Generating your optimized plan...'):
            bmi = calculate_bmi(weight, height)
            system_prompt = (
                "You are a performance optimization expert specializing in football. "
                "You provide detailed, structured, and personalized training, recovery, and diet strategies "
                "based on each player's physical and performance data. "
                "Always respond in markdown format using clear headings and bullet points."
            )

            user_prompt = f"""
📌 **Instruction**:
You must follow this exact structure:

---

### 🔍 Player Data Interpretation
Use bullet points. Interpret each of the following:
- Weight
- Height
- Energy Level
- Stress Level
- Sleep Quality
- Soreness Level
- Total Distance
- High-Speed Running
- Minutes per Session
- Number of Sprints
- BMI

Each bullet should be concise, clear, and actionable.

---

### 🏋️ Training Plan
Provide 3–5 bullet points personalized to the player's data.
Focus on volume, sprint frequency, endurance vs explosive needs, and practical drills.

---

### 🛌 Recovery Plan
Provide 3–5 recovery recommendations tailored to soreness, stress, and sleep levels.

---

### 🍽️ Diet Plan
Provide exact:
- Meal timing suggestions
- Macronutrient breakdowns (e.g., carbs, protein, fat grams)
- Food examples with portion sizes

Make it specific to the athlete’s weight, BMI, and training load.

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
- BMI: {bmi:.2f}  

---
⚠️ Avoid narrative or prose. Use only headings + bullet points as described.
Respond in markdown.
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
                placeholder.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

            # PDF download
            pdf_buffer = generate_pdf(response)
            st.download_button(
                label="📄 Download Plan as PDF",
                data=pdf_buffer,
                file_name="personalized_plan.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    display_personalized_plan()
