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

def display_personalized_plan():
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
            "You are a high-performance sports scientist and rehabilitation specialist working with elite athletes with disabilities. "
            "You receive detailed player data and must generate a safe, individualized training, recovery, diet, and supplement plan. "
            "You must fully adapt your output to the player's body composition (e.g., BMI), performance metrics, disability type, and classification. "
            "If the player has a high BMI or low training capacity, reduce training intensity, avoid joint overload, and scale caloric intake accordingly. "
            "If the disability impairs motor control (e.g., Ataxia), avoid unstable or dangerous exercises and focus on neuromuscular control. "
            "Your response must be clear, professional, and actionable."
        )



            user_prompt = f"""
            📌 **Instruction**:
            You must follow this exact structure. First, study the completed example below.
            Then, apply the same structure to the hidden player data that follows.

            Do **not repeat or display** the player data or disability profile. Use them only to inform your recommendations.

            ---

            ## ✅ Example Output (Use this structure exactly):

            ---

            ### 🧠 Context Summary:

            The athlete has a lower-limb impairment with classification suitable for unilateral sprinting. With a BMI of 24.07, their body composition is optimal for speed-focused training. However, sleep duration of only 6.5 hours and a pain level of 4/10 warrant moderate recovery emphasis. Their high training volume and elevated heart rate indicate the need for careful monitoring of fatigue and recovery balance.

            ---

            ### 🔍 Player Data Interpretation :

            - Weight (78 kg): Normal range; supports lean power output  
            - Height (180 cm): Biomechanically neutral  
            - Sleep Duration (6.5 hrs): Below optimal; may impair recovery  
            - Pain Scale (4/10): Moderate; monitor joint loading  
            - Distance Covered (5200 m): High aerobic work capacity  
            - Speed (5.8 m/s): Above average for amputee sprint class  
            - Acceleration (2.3 m/s²): Excellent, suggesting explosive power  
            - Training Volume (85 min/day): High; recovery load must scale  
            - Training Intensity (7/10): Matches volume well  
            - Heart Rate (152 bpm): Slightly elevated; monitor for fatigue  
            - BMI (24.07): Healthy range

            ---

            ### 🏋️ Training Plan :  
            **Brief:**  
            The athlete’s BMI, classification, and strong acceleration metrics justify a focus on explosive lower-body work. Given the moderate pain level and good training volume, training is balanced but avoids overuse stress.

            - Emphasize repeat sprints (30–40m), 3 sets x 5 reps  
            - Cap sprint volume under 700m/session to avoid fatigue  
            - Use 3:1 periodization (3 intense, 1 recovery week)  
            - Include unilateral strength training (glute/ham focus)  
            - Drill prosthetic balance and push-off mechanics

            ---

            ### 🛌 Recovery Plan :  
            **Brief:**  
            Recovery is guided by the athlete's suboptimal sleep (6.5 hrs) and pain score (4/10), with added attention to soft tissue and neurological recovery based on classification.

            - Contrast baths 2x/week after heavy sprint days  
            - Daily static stretching for hip/lower limb  
            - Add 30-min nap if <7 hrs of sleep  
            - Use massage gun (non-amputated limb) post-training  
            - Consider acetaminophen only when pain >5/10

            ---

            ### 🍽️ Diet Plan :  
            **Brief:**  
            The diet supports high training volume and normal BMI. Macronutrients are balanced to fuel performance and manage inflammation, with meal timing aligned to training load.

            - Meal timing: Carbs around training, protein evenly  
            - Daily kcal: ~2800  
            - Macros: 350g carbs, 150g protein, 75g fat  
            - Food examples:  
            - Breakfast: 2 boiled eggs + 1/2 cup oats + banana  
            - Lunch: 120g chicken breast + 1 cup brown rice + salad  
            - Dinner: 150g salmon + sweet potato + broccoli  
            - Snack: Protein bar or shake

            ---

            ### 💊 Supplement Plan :  
            **Brief:**  
            Supplementation targets joint support, muscle recovery, and anti-inflammatory effects. Selections are adapted to the athlete's classification and training stress markers.

            - Creatine Monohydrate – power – 5g/day post-workout  
            - Omega-3 – inflammation – 1g with dinner  
            - Vitamin D – bone health – 2000 IU daily  
            - Caffeine – optional pre-workout – 200mg  
            - Collagen + Vit C – joint/tendon support – 10g collagen + 50mg Vit C pre-training

            ---

            ⚠️ You MUST customize all recommendations to reflect:
            - The athlete's physical capability (e.g., overweight, motor impairment)
            - Their exact classification category
            - Their training load, pain, and recovery needs

            ## 🔍 Your Turn: Generate Plan

            Use the internal player data below. **Do not display or repeat it** in your output.

            📌 Additional Instructions:
            - **Always consider Disability Type and Classification** when generating training, recovery, diet, and supplement plans.
            - Highlight any red flags (e.g. high pain, low sleep, elevated heart rate).
            - Avoid exercises or supplements that are contraindicated for the given disability or classification.

            📌 Interpretation Instructions:
            - BMI ≥ 30 → Recommend low-impact cardio, caloric control, avoid joint overload.
            - Sleep < 7 hrs → Prioritize recovery, improve sleep hygiene, reduce training load.
            - Pain Scale ≥ 5 → Suggest pain-modulating strategies and training deloads.
            - Training Volume < 45 min/day → Avoid prescribing high-calorie diets or advanced programming.
            - Always analyze the **Disability Type and Classification** to shape:
            - Exercise safety (e.g., equipment needs, range of motion limits)
            - Functional capability (e.g., strength imbalance, limb use, spasticity)
            - Recovery needs (e.g., longer rest, assisted modalities)
            - Dietary and supplement support (e.g., bone health, inflammation, neurological support)

            📌 Output Requirements:
            - Start with a **Context Summary** paragraph (3–5 sentences).
            - Then write a short **brief (1–2 sentences)** before each of the five sections:
            - Explain how the player’s **BMI**, **disability type**, **classification**, **training volume**, **sleep**, and **pain** shape that part of the plan.
            - Then proceed with structured bullet-point recommendations.
            - Do not repeat or display raw input data.
            - No generalizations or fluff — tie all recommendations directly to the data.

            [DATA]  
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
            - Disability Type: {disability_type}  
            - Classification: {classification}  

            ---

            ### 🧠 Context Summary:

            ---

            ### 🔍 Player Data Interpretation :

            ---

            ### 🏋️ Training Plan :  
            **Brief:** Explain how BMI, disability, classification, and training load shape the plan.

            ---

            ### 🛌 Recovery Plan :  
            **Brief:** Explain how pain, sleep, classification, and fatigue risk influence the recovery strategy.

            ---

            ### 🍽️ Diet Plan :  
            **Brief:** Justify calorie amount and macro distribution based on BMI, volume, and recovery needs.

            ---

            ### 💊 Supplement Plan :  
            **Brief:** Justify supplements based on disability support (e.g., joints, inflammation, neural recovery).
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
                placeholder.markdown(response, unsafe_allow_html=False)


            pdf_buffer = generate_pdf(response)
            st.download_button(
                label="📄 Download Plan as PDF",
                data=pdf_buffer,
                file_name="personalized_plan.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    display_personalized_plan()
