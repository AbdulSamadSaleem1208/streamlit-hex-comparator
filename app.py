import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import os
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Hex Hash Value Predictor", page_icon="🔢", layout="centered")

# -------------------------------
# Custom CSS Styling (Modern Look)
# -------------------------------
st.markdown("""
<style>
/* Background gradient and layout */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 20%, #0f2027, #203a43, #2c5364);
    color: #ffffff;
}

/* Title */
.title {
    font-size: 2.7rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
}

/* Card container effect */
.block-container {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
}

/* Input field */
input {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #00C9FF !important;
    font-weight: 500;
}

/* Button styling */
div.stButton > button {
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    color: #000;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px #00C9FF;
    background: linear-gradient(90deg, #92FE9D, #00C9FF);
}

/* Alerts styling */
.stAlert {
    border-radius: 12px !important;
    font-weight: 600;
}

/* Remove Streamlit footer & menu */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown("<h1 class='title'>🔢 Hex Hash Value Predictor</h1>", unsafe_allow_html=True)

# -------------------------------
# Load Model
# -------------------------------
model_file_path = os.path.join(os.getcwd(), "fine_tuned_gradient_boosting_model (2).joblib")
loaded_model = None

try:
    loaded_model = joblib.load(model_file_path)
    st.success("✅ Model loaded successfully.")
except FileNotFoundError:
    st.error("❌ Model file not found! Please make sure the model file is in the same directory.")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")

# -------------------------------
# Feature Engineering Functions
# -------------------------------
def hex_to_bytes_features_single(h):
    h = h.lower()
    if len(h) < 64:
        h = h.rjust(64, '0')
    h = h[:64]
    return [int(h[i:i+2], 16) for i in range(0, 64, 2)]

def hash_numeric_summary_single(h):
    b = hex_to_bytes_features_single(h)
    arr = np.array(b, dtype=float)
    return [arr.mean(), arr.std(), arr.min(), arr.max(), arr.sum() % 256]

def hash_digit_freq_single(h):
    hex_digits = '0123456789abcdef'
    counts = [0] * 16
    for ch in h.lower():
        if ch in hex_digits:
            counts[hex_digits.index(ch)] += 1
    return counts

# -------------------------------
# Prediction Function
# -------------------------------
def predict_value_label_inference(hash_value, model):
    if model is None:
        return "Error: Model not loaded."

    byte_feats_single = np.array(hex_to_bytes_features_single(hash_value)).reshape(1, -1)
    freq_feats_single = np.array(hash_digit_freq_single(hash_value)).reshape(1, -1)
    extra_feats_single = np.array(hash_numeric_summary_single(hash_value)).reshape(1, -1)

    seed_val_single = pd.Series(pd.to_numeric(["0"], errors='coerce')).fillna(0).values.reshape(1, 1)

    X_single = np.hstack([seed_val_single, byte_feats_single, freq_feats_single, extra_feats_single])

    prediction = model.predict(X_single)[0]
    return "<=2.0" if prediction == 0 else ">2.0"

# -------------------------------
# Streamlit UI
# -------------------------------
st.subheader("Enter Hex Hash Value")
hash_input = st.text_input("Enter Hex Value:", placeholder="Example: f2e3447a8ee9a2b6428809cdb58d29")

if st.button("Predict"):
    if not hash_input:
        st.warning("⚠️ Please enter a hex value.")
    elif loaded_model is None:
        st.error("❌ Model not loaded.")
    else:
        with st.spinner("🔍 Processing your input..."):
            time.sleep(1.2)
            prediction = predict_value_label_inference(hash_input, loaded_model)
        if prediction == ">2.0":
            st.success(f"✅ Prediction: {prediction}")
        else:
            st.info(f"ℹ️ Prediction: {prediction}")
