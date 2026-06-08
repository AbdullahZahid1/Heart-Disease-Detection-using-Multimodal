import streamlit as st

st.title("Logging out...")
st.session_state['logged_in'] = False
st.switch_page("app.py")