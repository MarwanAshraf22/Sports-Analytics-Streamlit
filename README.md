# 🏋️‍♂️ Sports Analytics Project

This project applies sports analytics to improve performance, track health metrics, and provide data-driven insights for athletes. It combines wearable data, performance stats, and visualizations to support coaches and players in making informed decisions.

## 📌 Objectives

- Collect and analyze sports performance data (e.g., powerlifting, athletics)
- Visualize key metrics (e.g., training load, heart rate, recovery, sleep)
- Identify trends and areas of improvement
- Enable better decision-making for training and health
- Provide inclusive, tech-driven solutions for athletes
- Use machine learning to predict outcomes such as injuries, fatigue, and performance plateaus
- Use LLMs to personalize training, recovery, and diet plans

## 📊 Key Features

- 📈 Load monitoring and fatigue tracking using wearable devices data
- 🧠 Performance analytics (e.g., volume, intensity, PR trends)
- 🔮 ML-based predictions of injuries and performance outcomes
- 💡 Personalized insights and suggestions
- 🤖 LLM-driven recommendations for training, recovery, and nutrition


# Project Structure

### 📁 app/
- `app.py`, `home.py`: Main Streamlit app files.

### 📁 data/
- Raw: `calendar.csv`, `gps-data.csv`, `roster.csv`, `wellness.csv`
- Preprocessed: `*_preprocessed.csv`

### 📁 Images/
- App assets: logos and icons.

### 📁 models/
- `injury_risk_model.pkl`: Trained ML model.

### 📁 modules/
- `preprocessing/`: Clean data
- `predictions/`: Injury predictions
- `reporting/`: Reports (player/team)
- `personalization/`: Custom training plans

---
