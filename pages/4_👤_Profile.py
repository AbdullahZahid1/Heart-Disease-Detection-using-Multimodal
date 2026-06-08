import streamlit as st

# --- SECURITY CHECK ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page("app.py")

user_name = st.session_state.get('user_name', 'User')
user_role = st.session_state.get('role', 'patient')

# Display different titles based on role
if user_role == 'admin':
    st.title("👨‍⚕️ Provider Profile")
    st.write("Manage your clinical account settings and facility preferences.")
else:
    st.title("👤 Patient Profile")
    st.write("Manage your personal details and medical records.")

st.divider()

# --- DYNAMIC UI BASED ON ROLE ---
with st.container(border=True):
    st.subheader("Account Details")
    st.text_input("Full Name", value=user_name, disabled=True)
    
    # If the user is a DOCTOR (Admin)
    if user_role == 'admin':
        st.text_input("Hospital / Clinic Affiliation", placeholder="Enter facility name...")
        st.text_input("Specialization", placeholder="e.g., Cardiology, General Practice...")
        st.text_input("Medical License Number", placeholder="For official report generation...")
        
    # If the user is a PATIENT
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Age", min_value=1, max_value=120, value=30)
        with col2:
            st.selectbox("Biological Sex", ["Male", "Female"])
            
        st.text_input("Emergency Contact Name")
        st.text_input("Emergency Contact Phone")
    
    st.write("")
    st.button("Save Changes", type="primary")