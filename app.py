# app.py
import streamlit as st
from utils.model import predict_irrigation_need, predict_irrigation_schedule
from utils.crops import CROP_TYPES

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Irrigation System",
    page_icon="🌱",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {background-color: #f4f9f4;}
h1 {font-family: 'Trebuchet MS', sans-serif; color: #2e7d32;}
label, .stSelectbox, .stSlider {font-size: 16px;}
.result-box {padding: 15px; border-radius: 10px; background-color: #e8f5e9; font-size: 18px; font-weight: 600; color: black;}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🌾 Smart Irrigation System")
st.write("AI-powered decision support for sustainable farming")
st.divider()

# ---------- SIDEBAR ----------
st.sidebar.title("🌾 Smart Irrigation System")

with st.sidebar.expander("Project Description"):
    st.write(
        "Smart Irrigation Advisor is an AI-powered system that helps farmers decide "
        "whether irrigation is needed and adjusts irrigation intensity based on soil "
        "moisture, temperature, humidity, crop type, and rainfall data. The system "
        "aims to reduce water waste and promote sustainable agriculture."
    )

with st.sidebar.expander("SDG Impact"):
    st.write(
        "- SDG 2: Zero Hunger \n"
        "- SDG 6: Clean Water and Sanitation \n"
        "- SDG 12: Responsible Consumption and Production"
    )

with st.sidebar.expander("Tools Used"):
    st.write(
        "- Python\n"
        "- Streamlit\n"
        "- scikit-learn (Decision Tree Classifier)\n"
        "- NumPy\n"
        "- Pandas"
    )
  
st.sidebar.markdown("---")
st.sidebar.caption("Built by [Lakshitha M](https://github.com/lakshm22)")
# ---------- INPUTS ----------
soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 45)
temperature = st.slider("Temperature (°C)", 10, 45, 28)
humidity = st.slider("Humidity (%)", 20, 100, 60)
rainfall = st.slider("Recent Rainfall (mm)", 0, 50, 5)
crop_type = st.selectbox("Crop Type", CROP_TYPES)
st.divider()

# ---------- PREDICTION ----------
if st.button("Analyze Irrigation Need 🌱"):
    need = predict_irrigation_need(soil_moisture, temperature, humidity, crop_type)

    if need == 0:
        st.markdown(
            f"""
            <div class='result-box'>
            ✅ <b>No irrigation needed today.</b><br><br>
            Your soil moisture is <b>{soil_moisture}%</b> and recent rainfall was <b>{rainfall} mm</b>, 
            which is sufficient for your <b>{crop_type}</b> crop. 
            The temperature is {temperature}°C and humidity is {humidity}%, 
            creating favorable conditions. You can save water and let the soil retain moisture naturally.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(0)
        st.info("💧 Irrigation Level: 0% (No watering required)")

    else:
        schedule = predict_irrigation_schedule(soil_moisture, rainfall)
        schedule_map = {0: "⏸ Delay Irrigation", 1: "💧 Irrigate Lightly", 2: "🚿 Irrigate Fully"}

        # Calculate irrigation percentage for the gauge
        irrigation_percentage = max(0, min(100, (50 - soil_moisture) + (20 - rainfall)*2))
        irrigation_percentage = int(irrigation_percentage)

# Detailed result box
st.markdown(f"""
<div class='result-box'>
⚠ <b>Irrigation Required!</b><br><br>
Crop Type: <b>{crop_type}</b><br>
Soil Moisture: <b>{soil_moisture}%</b><br>
Recent Rainfall: <b>{rainfall} mm</b><br>
Temperature: <b>{temperature}°C</b>, Humidity: <b>{humidity}%</b><br><br>
Recommendation: <b>{schedule_map[schedule]}</b><br>
Approximate irrigation amount suggested: <b>{irrigation_percentage}% of standard irrigation volume</b>.<br><br>
This recommendation balances water use and crop needs to optimize growth while conserving water.
</div>
""", unsafe_allow_html=True)

# ---------- DYNAMIC GAUGE ----------
# More accurate: calculate percentage based on soil moisture & rainfall
irrigation_percentage = max(0, min(100, (50 - soil_moisture) + (20 - rainfall)*2))
irrigation_percentage = int(irrigation_percentage)

# Color coding
if irrigation_percentage <= 20:
    color = "green"
elif irrigation_percentage <= 60:
    color = "yellow"
else:
    color = "red"

st.markdown(f"""
<div style="border-radius:10px; background-color:#e0e0e0; height:25px; width:100%;">
<div style="width:{irrigation_percentage}%; background-color:{color}; height:25px; border-radius:10px;"></div>
</div>
""", unsafe_allow_html=True)
st.caption(f"💧 Irrigation Level: {irrigation_percentage}%")

st.markdown("---")
st.caption("Built for sustainability-focused decision making 🌍")
