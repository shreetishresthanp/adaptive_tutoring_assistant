import streamlit as st 

st.title("LSATLR Study")
st.write("Welcome to our Study! Please enter your name and group ID to begin.")

st.text_input("Name", key="name")
st.radio("Group ID", ["A", "B"], key="group_id")

start_btn = st.button("Start")

if start_btn:
  st.session_state.update({"name": st.session_state.name, "group_id": st.session_state.group_id})
  st.switch_page("pages/prequiz.py")
