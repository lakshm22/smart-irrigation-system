import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from utils.crops import CROP_TYPES

# ---------- CROP ENCODER ----------
crop_encoder = LabelEncoder()
crop_encoder.fit(CROP_TYPES)

# ---------- SYNTHETIC DATA GENERATION ----------
np.random.seed(42)

# Irrigation Need (Binary)
X_need = np.column_stack([
    np.random.randint(10, 90, 800),           # soil_moisture %
    np.random.randint(15, 40, 800),           # temperature C
    np.random.randint(30, 90, 800),           # humidity %
    crop_encoder.transform(np.random.choice(CROP_TYPES, 800))
])
y_need = ((X_need[:,0]<50) & (X_need[:,1]>25)).astype(int)

irrigation_need_model = DecisionTreeClassifier(max_depth=6, random_state=42)
irrigation_need_model.fit(X_need, y_need)

# Irrigation Schedule (Multiclass)
X_schedule = np.column_stack([
    np.random.randint(10, 90, 800),   # soil_moisture %
    np.random.randint(0, 50, 800)     # recent rainfall mm
])
y_schedule = np.zeros(800)
y_schedule[(X_schedule[:,0]<40) & (X_schedule[:,1]<10)] = 2   # Full
y_schedule[(X_schedule[:,0]<50) & (X_schedule[:,1]<20)] = 1   # Light
y_schedule[(X_schedule[:,0]>=50) | (X_schedule[:,1]>=20)] = 0 # Delay/No
y_schedule = y_schedule.astype(int)

irrigation_schedule_model = DecisionTreeClassifier(max_depth=5, random_state=42)
irrigation_schedule_model.fit(X_schedule, y_schedule)

# ---------- PREDICTION FUNCTIONS ----------
def predict_irrigation_need(soil_moisture, temperature, humidity, crop_type):
    crop_code = crop_encoder.transform([crop_type])[0]
    features = np.array([[soil_moisture, temperature, humidity, crop_code]])
    return irrigation_need_model.predict(features)[0]

def predict_irrigation_schedule(soil_moisture, rainfall):
    features = np.array([[soil_moisture, rainfall]])
    return irrigation_schedule_model.predict(features)[0]
