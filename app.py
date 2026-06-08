import streamlit as st
import sqlite3
import bcrypt
from utils.ui import apply_custom_ui
apply_custom_ui()


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CardioGuard AI | Portal", 
    page_icon="❤️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- LOAD CUSTOM CSS ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Fails gracefully if you haven't created style.css yet

load_css("style.css")

# --- DATABASE SETUP (Authentication & Roles) ---
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            email TEXT UNIQUE NOT NULL, 
            password_hash TEXT NOT NULL, 
            role TEXT NOT NULL
        )
    ''')
    
    # Safely upgrade older database tables to include the role column
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'patient'")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

init_db()

def verify_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, password_hash, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        name, stored_hash, role = user
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return name, role
    return None, None

def create_user(name, email, password, role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)", 
                       (name, email, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'view' not in st.session_state:
    st.session_state['view'] = 'landing' # Controls landing vs login routing

# If they are already logged in, instantly route to the Dashboard
if st.session_state['logged_in']:
    st.switch_page("pages/1_🏠_Dashboard.py")

# ==========================================
#               UI ROUTING
# ==========================================

# --- VIEW 1: LANDING PAGE ---
if st.session_state['view'] == 'landing':
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; font-size: 4.5rem; color: #d90429;'>❤️ CardioGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a1b0c0; font-weight: 300;'>Next-Generation Multimodal Cardiac Risk Assessment</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7a8b9f;'>Empowering clinicians with deep learning fused with ECG and clinical diagnostics.</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.session_state['view'] = 'login'
            st.rerun()

# --- VIEW 2: LOGIN / SIGNUP PAGE ---
elif st.session_state['view'] == 'login':
    st.title("Portal Access")
    
    if st.button("← Back to Home"):
        st.session_state['view'] = 'landing'
        st.rerun()
        
    with st.container(border=True):
        tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])
        
        with tab_login:
            with st.form("login_form"):
                login_email = st.text_input("Email Address")
                login_password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Log In", use_container_width=True):
                    user_name, user_role = verify_user(login_email, login_password)
                    if user_name:
                        st.session_state['logged_in'] = True
                        st.session_state['user_name'] = user_name
                        st.session_state['role'] = user_role
                        st.rerun()
                    else:
                        st.error("Incorrect Email or Password.")
        
        with tab_signup:
            with st.form("signup_form"):
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email Address")
                new_password = st.text_input("Create Password", type="password")
                
                account_type = st.selectbox("Account Type", ["Patient", "Medical Professional (Admin)"])
                role = "admin" if "Admin" in account_type else "patient"
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        success = create_user(new_name, new_email, new_password, role)
                        if success:
                            st.success("Account created successfully! Switch to the Log In tab.")
                        else:
                            st.error("An account with that email already exists.")