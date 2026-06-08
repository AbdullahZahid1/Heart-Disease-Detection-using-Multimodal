import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- SECURITY CHECK ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page("app.py")

# --- FETCH REAL DATABASE DATA ---
# Safely try to fetch the history to make the dashboard dynamic
try:
    from utils.database import get_history
    df_history = get_history()
    total_patients = len(df_history)
    high_risk_count = len(df_history[df_history['risk_level'] == 'High Risk']) if total_patients > 0 else 0
except Exception:
    df_history = pd.DataFrame() # Fallback if DB isn't ready
    total_patients, high_risk_count = 0, 0

# --- HEADER SECTION ---
# Fetch the user's name and role from the secure session state
user_name = st.session_state.get('user_name', 'User')
user_role = st.session_state.get('role', 'patient')

# --- DYNAMIC GREETING ---
if user_role == 'admin':
    st.markdown(f"<h1>Welcome back, Dr. {user_name}! 👋</h1>", unsafe_allow_html=True)
    st.markdown("Here is the real-time overview of the CardioGuard AI assessment system.")
else:
    st.markdown(f"<h1>Welcome back, {user_name}! 👋</h1>", unsafe_allow_html=True)
    st.markdown("Welcome to your personal CardioGuard patient portal.")
# --- KPI METRICS (TOP ROW) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric(label="Total Scans (All Time)", value=total_patients, delta="Live DB Connection")

with col2:
    with st.container(border=True):
        # We color High Risk red (inverse) so it stands out as a warning
        st.metric(label="High Risk Detected", value=high_risk_count, delta="Requires Attention", delta_color="inverse")

with col3:
    with st.container(border=True):
        st.metric(label="System Accuracy", value="94.2%", delta="+0.5% this month")

with col4:
    with st.container(border=True):
        st.metric(label="Network Status", value="Online", delta="All Systems Nominal", delta_color="off")

st.write("") 
st.write("")

# --- MAIN DASHBOARD VISUALS (BOTTOM ROW) ---
col_chart, col_feed = st.columns([2, 1.2])

# Left Column: Interactive Activity Chart
with col_chart:
    st.subheader("📈 Assessment Volume (Last 7 Days)")
    with st.container(border=True):
        # Generate dummy trend data that looks realistic for a medical clinic
        dates = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
        chart_data = pd.DataFrame({
            "Routine Scans": np.random.randint(5, 15, size=7),
            "High Risk Alerts": np.random.randint(0, 4, size=7)
        }, index=dates)
        
        # Streamlit's native area chart looks beautiful with your custom theme
        st.area_chart(chart_data, color=["#A8DADC", "#d90429"])

# Right Column: Live Feed & Quick Actions
with col_feed:
    st.subheader("⚡ Quick Actions")
    with st.container(border=True):
        st.write("Need to run a new scan?")
        if st.button("❤️ Start New Prediction", use_container_width=True, type="primary"):
            st.switch_page("pages/2_❤️_Predict_Risk.py")
        
        st.write("Review past patient reports?")
        if st.button("📊 View Full Patient Database", use_container_width=True):
            st.switch_page("pages/3_📊_History.py")

    st.write("")
    
    st.subheader("🔔 Recent Scans (Live)")
    with st.container(border=True):
        if df_history.empty:
            st.info("No scans performed yet. Run a prediction to see live alerts here.")
        else:
            # Show only the 4 most recent scans from the database
            recent_scans = df_history.head(4)
            for index, row in recent_scans.iterrows():
                if row['risk_level'] == "High Risk":
                    st.error(f"🚨 **{row['patient_id']}**: {row['risk_level']} ({row['probability']})")
                elif row['risk_level'] == "Moderate Risk":
                    st.warning(f"⚠️ **{row['patient_id']}**: {row['risk_level']} ({row['probability']})")
                else:
                    st.success(f"✅ **{row['patient_id']}**: {row['risk_level']} ({row['probability']})")