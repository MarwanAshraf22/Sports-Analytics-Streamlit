import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
from .generate_pdf import generate_pdf

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load player data
player_df = pd.read_csv("data/players_data.csv")

def calculate_bmi(weight, height):
    if weight > 0 and height > 0:
        return weight / (height / 100) ** 2
    return 0

def display_pod_plan():
    st.markdown(
        """
        <style>
        body { font-family: 'Dubai', sans-serif; }
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
        .response-box ul { margin-left: 20px; }
        </style>
        <div class="title-box">🏅 Personalized Plan for People of Determination 🏅</div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Select a player to load their performance and wellness data.")

    player_name = st.selectbox("Select Player", player_df['Player Name'].unique())
    player_data = player_df[player_df['Player Name'] == player_name].iloc[0]

    if player_data.isnull().any():
        st.warning("⚠️ Some data fields are missing for this player. Please review the dataset.")

    # Extract player metrics
    height = player_data['Height']
    weight = player_data['Weight']
    classification = player_data['Classification Category']
    disability_type = player_data['Disability Type']
    speed = player_data['Speed (m/s)']
    acceleration = player_data['Acceleration']
    distance = player_data['Distance Covered (m)']
    training_volume = player_data['Training Volume (min/day)']
    training_intensity = player_data['Training Intensity (1–10)']
    heart_rate = player_data['Heart Rate (bpm)']
    sleep = player_data['Sleep Duration (hrs)']
    pain_scale = player_data['Pain Scale']
    bmi = calculate_bmi(weight, height)

    # Show player metrics
    st.markdown(f"<div class='section-header'>📋 Loaded Data for: {player_name}</div>", unsafe_allow_html=True)
    player_table = pd.DataFrame([{
        "Height (cm)": height,
        "Weight (kg)": weight,
        "BMI": round(bmi, 2),
        "Classification": classification,
        "Disability Type": disability_type,
        "Speed (m/s)": speed,
        "Acceleration (m/s²)": acceleration,
        "Distance (m)": distance,
        "Training Volume (min/day)": training_volume,
        "Training Intensity": training_intensity,
        "Heart Rate (bpm)": heart_rate,
        "Sleep (hrs)": sleep,
        "Pain Scale": pain_scale
    }])
    st.dataframe(player_table, use_container_width=True)

    st.markdown("---")

    if st.button('🚀 Generate Personalized Plan', use_container_width=True):
        with st.spinner('🧠 Generating your personalized plan...'):

            system_prompt = (
                "You are a sports performance specialist for athletes with disabilities. "
                "Given structured data, generate a detailed and personalized training, recovery, diet, and supplement plan. "
                "Always use markdown format with clear headers and bullet points."
            )

            user_prompt = f"""
📌 **Instruction**:
You must follow this exact structure:

---

### 🔍 Real Player Data:
- Weight: {weight} kg  
- Height: {height} cm  
- Sleep Duration: {sleep} hrs  
- Pain Scale: {pain_scale}/10  
- Distance Covered: {distance} m  
- Speed: {speed} m/s  
- Acceleration: {acceleration} m/s²  
- Training Volume: {training_volume} min/day  
- Training Intensity: {training_intensity}/10  
- Heart Rate: {heart_rate} bpm  
- BMI: {bmi:.2f}  

---

### ♿ Disability Profile
- Disability Type: {disability_type}  
- Classification: {classification}  

These characteristics define the athlete’s physical constraints and must influence every recommendation that follows.

---

### 🔍 Player Data Interpretation
Use bullet points. Interpret each of the following:
- Weight
- Height
- Sleep Duration
- Pain Scale
- Distance Covered
- Speed
- Acceleration
- Training Volume
- Training Intensity
- Heart Rate
- BMI

Each bullet should be concise, clear, and actionable. Link metrics to functional or physiological implications.

---

### 🏋️ Training Plan
Provide bullet points personalized to the player's data.
Focus on:
- Sprint frequency and distance thresholds
- Volume vs. intensity balance
- Periodization considerations
- Technical vs. physical load emphasis
- Sport-specific drills

---

### 🛌 Recovery Plan
Provide recovery recommendations tailored to pain, sleep, and training intensity.
Include:
- Modalities (e.g., cold water, stretching)
- Frequency
- Passive vs. active strategies
- Pain management adjustments

---

### 🍽️ Diet Plan
Provide:
- Meal timing
- Daily kcal estimates
- Macronutrient breakdowns in grams (carbs, protein, fats)
- Food examples with portion sizes (e.g., 120g chicken breast, 1/2 cup oats)

Base all on body composition and training load.

---

### 💊 Supplement Plan
List supplement recommendations with:
- Supplement name
- Purpose
- Suggested dosage/timing
- Any disability-specific or anti-doping considerations

---

### ♿ Disability-Specific Considerations
Provide 3–5 bullet points that:
- Describe how the athlete’s disability type and classification affect physical capacity or movement
- Identify any constraints for training, nutrition, recovery, or supplementation
- Recommend necessary safety or technique modifications

---

⚠️ Avoid narrative or prose. Use only headings + bullet points as described.
Respond in markdown. Ensure that all recommendations (training, recovery, diet, supplements) are tailored based on disability type, physical limitations, and classification when relevant.
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
                st.error("❌ Unable to generate plan. Please check your API key or try again later.")
                return

            response = ""
            placeholder = st.empty()
            for chunk in stream:
                response += chunk.choices[0].delta.content or ''
                placeholder.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

            pdf_buffer = generate_pdf(response)
            st.download_button(
                label="📄 Download Plan as PDF",
                data=pdf_buffer,
                file_name="personalized_plan_POD.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    display_pod_plan()
