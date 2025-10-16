import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# -------------------------------
# Page Title
# -------------------------------
st.set_page_config(page_title="Hex Hash Value Predictor", page_icon="🔢", layout="centered")
st.title("🔢 Hex Hash Value Predictor")

# -------------------------------
# Load Model
# -------------------------------
# Automatically locate the model file in the same folder
model_file_path = os.path.join(os.getcwd(), "fine_tuned_gradient_boosting_model (2).joblib")

loaded_model = None
try:
    loaded_model = joblib.load(model_file_path)
    st.success("✅ Model loaded successfully.")
except FileNotFoundError:
    st.error("❌ Model file not found! Please make sure 'fine_tuned_gradient_boosting_model (2).joblib' is in the same directory.")
except Exception as e:
    st.error(f"❌ An error occurred while loading the model: {e}")

# -------------------------------
# Feature Engineering Functions
# -------------------------------
def hex_to_bytes_features_single(h):
    h = h.lower()
    if len(h) < 64:
        h = h.rjust(64, '0')
    h = h[:64]
    return [int(h[i:i+2],16) for i in range(0,64,2)]

def hash_numeric_summary_single(h):
    b = hex_to_bytes_features_single(h)
    arr = np.array(b, dtype=float)
    return [arr.mean(), arr.std(), arr.min(), arr.max(), arr.sum()%256]

def hash_digit_freq_single(h):
    hex_digits = '0123456789abcdef'
    counts = [0]*16
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

    byte_feats_single  = np.array(hex_to_bytes_features_single(hash_value)).reshape(1, -1)
    freq_feats_single  = np.array(hash_digit_freq_single(hash_value)).reshape(1, -1)
    extra_feats_single = np.array(hash_numeric_summary_single(hash_value)).reshape(1, -1)

    # Placeholder seed feature
    seed_val_single = pd.Series(pd.to_numeric(["0"], errors='coerce')).fillna(0).values.reshape(1,1)

    # Combine all features
    X_single = np.hstack([seed_val_single, byte_feats_single, freq_feats_single, extra_feats_single])

    # Predict
    prediction = model.predict(X_single)[0]
    return "<=2.0" if prediction == 0 else ">2.0"

# -------------------------------
# Streamlit UI
# -------------------------------
st.header("Enter Hex Hash Value")
hash_input = st.text_input("Enter Hex Value:", placeholder="Example: f2e3447a8ee9a2b6428809cdb58d29")

if st.button("Predict"):
    if not hash_input:
        st.warning("⚠️ Please enter a hex value.")
    elif loaded_model is None:
        st.error("❌ Model not loaded. Please check the file.")
    else:
        prediction = predict_value_label_inference(hash_input, loaded_model)
        st.success(f"✅ Prediction: {prediction}")

st.caption("Built with ❤️ using Streamlit | Developed by Usman & Team")

