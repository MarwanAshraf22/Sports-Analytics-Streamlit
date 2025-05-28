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

            system_prompt = (
                "You are a performance optimization expert specializing in football. "
                "You provide detailed, structured, and personalized training, recovery, and diet strategies "
                "based on each player's physical and performance data."
                "Always respond in markdown format using clear headings and bullet points."
            )


            user_prompt = f"""
            📌 **Instruction**: Analyze the player's data below and generate a detailed plan using the same structure and tone as the example. Always format your response in markdown.

            ---

            ### ✅ Example Player Data:
            - Weight: 75 kg  
            - Height: 180 cm  
            - Energy Level: High  
            - Stress Level: Low  
            - Sleep Quality: Excellent  
            - Soreness Level: Low  
            - Total Distance: 8.5 km  
            - High-Speed Running: 2.0 km  
            - Minutes per Session: 70  
            - Number of Sprints: 12  
            - BMI: 23.1  

            ### 📝 Example Output:

            *** Here is your personalized performance, recovery, and nutrition plan: ***

            🏋️ **Training Plan**
            - **Focus Areas**: Stamina, Speed, Endurance  
            - **Exercise Recommendations**:  
            - Sprint intervals (6 x 100m at 90% max speed)  
            - Tempo runs (20 minutes at moderate pace)  
            - Agility ladder drills (3 sets, 30s each)  
            - Bulgarian split squats (3 sets x 10 reps/leg)  
            - Core circuit (planks, leg raises, Russian twists – 3 rounds)  
            - **Weekly Training Hours**: 6–7 hours/week  
            - **Performance Goals**: Improve sprint frequency and maintain high-speed running capacity

            🛌 **Recovery Plan**
            - **Rest Days**: 2 days/week  
            - **Recovery Techniques**: Foam rolling, light cycling, contrast water therapy  
            - **Sleep Recommendations**: 8 hours/night, sleep by 10:30 PM, avoid screens 1 hour before bed  
            - **Additional Restorative Practices**: Post-training stretching, yoga once per week, 10-min daily meditation

            🍽️ **Diet Plan**
            - **Daily Caloric Intake**: 2800 kcal/day  
            - **Macronutrient Breakdown**: 50% Carbs / 25% Protein / 25% Fat  
            - **Hydration**: 3 liters of water/day  
            - **Sample Meals**:  
            - **Breakfast**: Oats with banana, almond butter, and protein shake  
            - **Lunch**: Grilled chicken, quinoa, steamed broccoli  
            - **Dinner**: Baked salmon, sweet potato, and avocado salad  
            - **Snacks**: Greek yogurt with honey, nuts, rice cakes with peanut butter

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
            - Be detailed but concise.
            - Use bullet points for clarity.
            - Follow the exact structure shown in the example.
            - Tailor recommendations to the player’s data.
            - Keep tone professional, supportive, and motivating.

            *** Now generate the plan using the structure above. ***
            """


            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream = True
            )

            response = ""
            placeholder = st.empty()
            for chunk in stream:
                response += chunk.choices[0].delta.content or ''
                placeholder.markdown(response)

            # ---- Download as PDF ----
            pdf = generate_pdf(response)
            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf,
                file_name="personalized_plan.pdf",
                mime="application/pdf"
            )
