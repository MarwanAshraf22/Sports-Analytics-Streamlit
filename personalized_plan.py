import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import io

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to calculate BMI
def calculate_bmi(weight, height):
    if weight > 0 and height > 0:
        return weight / (height / 100) ** 2  # Convert height from cm to meters
    return 0

# Function to generate PDF
def generate_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))  # Use landscape orientation
    width, height = landscape(letter)  # Get landscape dimensions
    y = height - 50

    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

# Function to display the personalized plan
def display_personalized_plan():
    st.markdown(
        """
        <style>
        .report-title {
            font-size: 40px;
            font-weight: bold;
            color: #003399;
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
        <div class="report-title">⚽ Real Madrid Player Personalization Tool ⚽</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="subtext">Fill out the form below to get your personalized training, recovery, and diet plan.</p>', unsafe_allow_html=True)

    # ---- Player Physical Data ----
    st.markdown('<div class="section-title">📊 Player Physical Data</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input('Weight (kg)', min_value=60)
    with col2:
        height = st.number_input('Height (Cm)', min_value=100)

    bmi = calculate_bmi(weight, height)
    st.success(f'✅ BMI: **{bmi:.2f}**')

    # ---- Performance Data ----
    st.markdown('<div class="section-title">📈 Performance Metrics</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        energy = st.slider('⚡ Energy Level', 1, 10)
        stress = st.slider('😣 Stress Level', 1, 10)
    with col4:
        sleep_quality = st.slider('💤 Sleep Quality', 1, 10)
        soreness = st.slider('💪 Soreness Level', 1, 10)

    # ---- Session & Sprint Data ----
    st.markdown('<div class="section-title">🏃 Session & Sprint Data</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        total_distance = st.number_input('Total Distance (km)', min_value=0.0)
        minutes_per_session = st.number_input('Minutes per Session', min_value=0)
    with col6:
        high_speed_running = st.number_input('High-Speed Running (km)', min_value=0.0)
        num_sprints = st.number_input('Number of Sprints', min_value=0)

    # ---- Generate Button ----
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button('🚀 Generate Personalized Plan', use_container_width=True):
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

            prompt = f"""
                
                You are a professional sports performance expert. Based on the following player's physical and performance data, generate a structured and detailed plan in the following format:
                
                *** Here is your personalized performance, recovery, and nutrition plan: ***

                🏋️ **Training Plan**
                - **Focus Areas**: (e.g., Strength, Agility, Stamina, etc. based on the player's performance data)
                - **Exercise Recommendations**: (List 3-5 exercises with sets, reps, and intensity recommendations)
                - **Weekly Training Hours**: (e.g., X hours/week. Tailor based on energy level and soreness)
                - **Performance Goals**: (e.g., Improve total distance, high-speed running, or sprints)

                🛌 **Recovery Plan**
                - **Rest Days**: (e.g., 2-3 days/week depending on soreness and stress levels)
                - **Recovery Techniques**: (e.g., Massage, cryotherapy, active recovery, etc. customized for the player’s recovery needs)
                - **Sleep Recommendations**: (e.g., Bedtime routine, optimal sleep duration for recovery and performance)
                - **Additional Restorative Practices**: (e.g., Stretching, light recovery exercises, mindfulness)

                🍽️ **Diet Plan**
                - **Daily Caloric Intake**: (e.g., XXXX kcal/day based on weight, BMI, and energy needs)
                - **Macronutrient Breakdown**: (e.g., XX% Carbs / XX% Protein / XX% Fat for optimal performance and recovery)
                - **Hydration**: (e.g., 3 liters of water/day or more depending on the intensity of activity)
                - **Sample Meals**: 
                    - Breakfast: (e.g., Protein-rich, high-carb meal for energy)
                    - Lunch: (e.g., Balanced meal with lean protein and complex carbs)
                    - Dinner: (e.g., Light, easily digestible protein source with healthy fats)
                    - Snacks: (e.g., Energy-boosting snacks for recovery or pre-workout)

                Now generate a plan for this player:

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

                Be detailed but concise. Use bullet points for clarity and ensure each section follows the format above. Tailor the plan to the player’s current condition and optimize for future performance.

            """


            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a performance optimization expert, helping football players with personalized training, recovery, and diet strategies."},
                    {"role": "user", "content": prompt}
                ]
            )

            plan = completion.choices[0].message.content

            st.markdown('<div class="section-title">📋 Personalized Plan</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="plan-content">{plan}</div>', unsafe_allow_html=True)

            # ---- Download as PDF ----
            pdf = generate_pdf(plan)
            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf,
                file_name="personalized_plan.pdf",
                mime="application/pdf"
            )

# Run the app
display_personalized_plan()
