import streamlit as st
import pandas as pd

# Import our database helper function!
from utils.database import get_history 

# --- SECURITY CHECK ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page("app.py")

# --- UI HEADER ---
st.title("📊 Patient Prediction History")
st.markdown("All completed multimodal risk assessments are securely logged below.")
st.divider()

# --- FETCH REAL DATABASE DATA ---
try:
    # This pulls the actual saved predictions from data/prediction_history.db
    history_df = get_history()
    
    if history_df.empty:
        # What to show if the database is empty
        st.info("No predictions have been made yet. Head over to the 'Predict Risk' page to run your first scan!")
    else:
        # Streamlit draws a beautiful, interactive table automatically
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Optional: Add a quick download button for the raw CSV data
        st.write("")
        csv = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full History as CSV",
            data=csv,
            file_name='clinic_assessment_history.csv',
            mime='text/csv',
        )
        
except Exception as e:
    st.error(f"Could not connect to the local database. Ensure the 'utils' folder is set up correctly. Error: {e}")