import streamlit as st 
from utils.firebase_util import init_connection
init_connection()

st.title("LSATLR Study")
st.write("Welcome to our Study! Please enter your name and group ID to begin.")

name =st.text_input("Name")
group_id = st.radio("Group ID", ["A", "B"])

start_btn = st.button("Start")

if start_btn:
  st.session_state.name = name
  st.session_state.group_id = group_id
  st.switch_page("pages/presurvey.py")
