import streamlit as st
import pandas as pd
import joblib

# 1. Load your model (ensure the file name matches exactly)
# Make sure Fraud_Detection_Model.joblib is in the same folder as this script!
model = joblib.load('Fraud_Detection_Model.joblib')

st.set_page_config(page_title="Fraud Guard", page_icon="🛡️")

st.title("🛡️ Transaction Fraud Analysis")
st.write("Input the transaction details below to evaluate the risk level.")

# Create two columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial & Time")
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=1.0)
    t_hour = st.slider("Hour of Day (0-23)", 0, 23, 12)
    velocity = st.number_input("Transactions in Last 24h", min_value=0, step=1)
    merchant = st.selectbox("Merchant Category", options=[0, 1, 2, 3]) # Replace with your encoded categories

with col2:
    st.subheader("Security & Profile")
    age = st.number_input("Cardholder Age", min_value=18, max_value=100, value=30)
    device_score = st.slider("Device Trust Score", 0.0, 1.0, 0.8)
    
    # Booleans/Flags
    foreign = st.toggle("Foreign Transaction")
    mismatch = st.toggle("Location Mismatch")

# Predict Button
if st.button("Run Fraud Check", type="primary"):
    # 1. Prepare data (ID is excluded; boolean converted to 1/0)
    # Order must match your training set!
    input_data = pd.DataFrame([[
        amount, t_hour, merchant, 
        int(foreign), int(mismatch), device_score, 
        velocity, age
    ]], columns=[
        'amount', 'transaction_hour', 'merchant_category',
        'foreign_transaction', 'location_mismatch', 'device_trust_score',
        'velocity_last_24h', 'cardholder_age'
    ])

    # 2. Get Prediction (Probability of fraud)
    prob = model.predict_proba(input_data)[0][1]
    
    # 3. Display Results
    st.divider()
    if prob > 0.7:
        st.error(f"### 🚨 HIGH RISK: {prob:.1%}")
        st.warning("Action: Decline transaction and alert cardholder.")
    elif prob > 0.3:
        st.warning(f"### ⚠️ MEDIUM RISK: {prob:.1%}")
        st.info("Action: Trigger secondary authentication (OTP).")
    else:
        st.success(f"### ✅ LOW RISK: {prob:.1%}")
        st.write("Action: Approve transaction.")