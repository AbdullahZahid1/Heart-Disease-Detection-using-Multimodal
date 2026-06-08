import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from Ecg import ECG
from utils.ui import apply_custom_ui
from datetime import datetime

# --- UTILITIES ---
from utils.database import save_prediction, get_next_patient_id
from utils.pdf_maker import generate_pdf_report

apply_custom_ui()

# --- SECURITY CHECK ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page("app.py")

# --- LOAD AI MODELS ---
@st.cache_resource
def load_clinical_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    model_path = os.path.join(parent_dir, "xgboost_model.pkl") 
    
    with open(model_path, "rb") as file:
        return joblib.load(file) 

xgboost_model = load_clinical_model()
ecg_model = ECG() 

# --- UI HEADER ---
st.title("❤️ Multimodal Risk Assessment")
st.markdown("Enter the clinical markers and upload the corresponding ECG to generate a unified risk score.")

# --- 1. CLINICAL DATA INPUTS ---
st.subheader("1. Patient Clinical Data")

with st.container(border=True):
    st.markdown("**Basic Demographics & Vitals**")
    
    # Fetch the auto-generated "Primary Key" ID safely
    try:
        auto_patient_id = get_next_patient_id()
    except Exception:
        auto_patient_id = f"PT-{np.random.randint(1000, 9999)}"
        
    col_id, col_name = st.columns(2)
    with col_id:
        st.text_input("System Assigned Patient ID", value=auto_patient_id, disabled=True)
    with col_name:
        patient_name = st.text_input("Patient Full Name", placeholder="e.g., John Doe")
        
    st.write("") # Spacing
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: age = st.number_input("Age", 1, 120, 45)
    with col2: sex = st.selectbox("Biological Sex", [0, 1], format_func=lambda x: "Female" if x==0 else "Male")
    with col3: trestbps = st.number_input("Resting BP (mmHg)", value=120)
    with col4: thalach = st.number_input("Max Heart Rate", value=150)

with st.container(border=True):
    st.markdown("**Bloodwork & Pain Indicators**")
    col1, col2, col3 = st.columns(3)
    with col1: chol = st.number_input("Cholesterol (mg/dl)", value=180)
    with col2: fbs = st.selectbox("Fasting Blood Sugar", [0, 1], format_func=lambda x: "Normal" if x==0 else "High")
    with col3: cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], index=3, format_func=lambda x: ["Typical Angina", "Atypical", "Non-anginal", "Asymptomatic"][x])
    with col1: exang = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")

with st.container(border=True):
    st.markdown("**Advanced ECG & Angiography Metrics**")
    col1, col2, col3, col4 = st.columns(4)
    with col1: restecg = st.selectbox("Resting ECG", [0, 1, 2])
    with col2: oldpeak = st.number_input("ST Depression", value=0.0, step=0.1)
    with col3: slope = st.selectbox("ST Slope", [0, 1, 2], index=2)
    with col4: ca = st.selectbox("Major Vessels", [0, 1, 2, 3, 4], index=0)
    thal = st.selectbox("Thalassemia", [0, 1, 2, 3], index=2)

st.write("") 

# --- 2. ECG UPLOAD SECTION ---
st.subheader("2. Electrocardiogram Imaging")
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload 12-Lead ECG Image", type=["jpg", "jpeg", "png"])

# --- 3. EXECUTION BUTTON ---
st.write("")
analyze_btn = st.button("Analyze Multimodal Data", type="primary", use_container_width=True)

if analyze_btn:
    if uploaded_file is None:
        st.warning("Please upload an ECG image to proceed.")
    else:
        with st.spinner("Fusing Clinical and ECG Models. This may take a moment..."):
            
            # A. Process Clinical Data
            clinical_data = pd.DataFrame({
                'age': [age], 'sex': [sex], 'cp': [cp], 'trestbps': [trestbps], 
                'chol': [chol], 'fbs': [fbs], 'restecg': [restecg], 'thalach': [thalach],
                'exang': [exang], 'oldpeak': [oldpeak], 'slope': [slope], 'ca': [ca], 'thal': [thal]
            }) 
            
            raw_clinical_probs = xgboost_model.predict_proba(clinical_data)
            clinical_probs_arr = np.array(raw_clinical_probs).flatten()
            
            # B. Process ECG Data
            ecg_user_image_read = ecg_model.getImage(uploaded_file)
            dividing_leads = ecg_model.DividingLeads(ecg_user_image_read)
            ecg_model.PreprocessingLeads(dividing_leads)
            ecg_model.SignalExtraction_Scaling(dividing_leads)
            ecg_1dsignal = ecg_model.CombineConvert1Dsignal()
            ecg_final = ecg_model.DimensionalReduciton(ecg_1dsignal)
            
            raw_ecg_probs = ecg_model.ModelLoad_predict(ecg_final)
            ecg_probs_arr = np.array(raw_ecg_probs).flatten()
            
            # --- NEW: EXACT 4-CLASS ECG EXTRACTION ---
            # IMPORTANT: I assumed "Normal" is at index [2] based on your old code. 
            # If your CNN classes are in a different order, change this list!
            ecg_class_names = ["Abnormal Heartbeat", "History of MI", "Normal", "Myocardial Infarction"]
            
            predicted_index = np.argmax(ecg_probs_arr)
            ecg_status = ecg_class_names[predicted_index]
            ecg_confidence = ecg_probs_arr[predicted_index] * 100
            
            # C. Smart Clinical Late Fusion
            clinical_prob_disease = clinical_probs_arr[1]
            ecg_prob_disease = 1.0 - ecg_probs_arr[2]  # Probability that it is NOT normal
            
            highest_risk = max(clinical_prob_disease, ecg_prob_disease)
            lowest_risk = min(clinical_prob_disease, ecg_prob_disease)
            
            fused_prob_disease = (highest_risk * 0.75) + (lowest_risk * 0.25)
            overall_disease_risk_percentage = fused_prob_disease * 100 
            
            st.divider()
            
            # --- NEW: DISPLAY STANDALONE ECG STATUS ---
            st.subheader("Cardiogram Image Analysis")
            if ecg_status == "Normal":
                st.success(f"🩺 **Detected ECG Class:** {ecg_status}  \n**AI Confidence:** {ecg_confidence:.1f}%")
            else:
                st.error(f"⚠️ **Detected ECG Class:** {ecg_status}  \n**AI Confidence:** {ecg_confidence:.1f}%")
                
            st.write("") # Spacing
            
            # D. The Red Flag Override
            if clinical_prob_disease >= 0.75 or ecg_prob_disease >= 0.75:
                risk_level, st_color, icon = "High Risk", "#e76f51", "🚨"
                overall_disease_risk_percentage = max(overall_disease_risk_percentage, highest_risk * 100)
            elif overall_disease_risk_percentage < 40:
                risk_level, st_color, icon = "Low Risk", "#2a9d8f", "✅"
            elif overall_disease_risk_percentage < 75:
                risk_level, st_color, icon = "Moderate Risk", "#e9c46a", "⚠️"
            else:
                risk_level, st_color, icon = "High Risk", "#e76f51", "🚨"
            
            # Results UI
            st.markdown(f"""
            <div style="background-color: {st_color}15; padding: 2rem; border-radius: 10px; border-left: 10px solid {st_color}; text-align: center;">
                <h1 style="color: {st_color}; margin-bottom: 0;">{icon} {risk_level}</h1>
                <p style="font-size: 1.2rem; color: #555;">Overall Multimodal Risk Probability</p>
                <h1 style="font-size: 4rem; margin-top: 0;">{overall_disease_risk_percentage:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.progress(overall_disease_risk_percentage / 100.0)
            
            # Live AI Debugger
            with st.expander("🔍 View Raw AI Model Breakdown"):
                st.write("**Clinical Data Model (XGBoost):**")
                st.info(f"Calculated Risk: **{clinical_prob_disease * 100:.1f}%**")
                st.write("**ECG Image Model (CNN):**")
                st.info(f"Calculated Risk: **{ecg_prob_disease * 100:.1f}%**")

            # --- DATABASE SAVE & PDF ---
            final_name = patient_name.strip() if patient_name.strip() != "" else "Anonymous Patient"
            
            # This line handles your database seamlessly!
            save_prediction(auto_patient_id, final_name, risk_level, f"{overall_disease_risk_percentage:.1f}%")
            
            pdf_bytes = generate_pdf_report(
                patient_name=f"{auto_patient_id} | {final_name}", 
                age=age, 
                sex="Male" if sex==1 else "Female", 
                risk_level=risk_level, 
                probability=overall_disease_risk_percentage, 
                clinical_prob=clinical_prob_disease*100, 
                ecg_prob=ecg_prob_disease*100
            )
            
            st.write("")
            st.download_button(
                label="📄 Download Official PDF Report",
                data=pdf_bytes,
                file_name=f"CardioGuard_Report_{auto_patient_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )